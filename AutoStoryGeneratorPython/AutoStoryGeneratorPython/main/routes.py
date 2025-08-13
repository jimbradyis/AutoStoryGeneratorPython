"""
Routes for the main blueprint.
"""
import math
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, abort
from ...models.story import Story, WorldBuilderEntry, Character
from ...services.llm_service import generate_text

# Create the main blueprint
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='../templates',
    static_folder='../static'
)

# In-memory store for stories. In a real app, this would be a database.
stories = {}


@main_bp.route('/', methods=['GET', 'POST'])
def home():
    """Renders the home page and handles form submission to start story generation."""
    if request.method == 'POST':
        story_data = {
            'prompt': request.form.get('prompt'),
            'main_character_desc': request.form.get('main_character_desc'),
            'target_length': int(request.form.get('target_length')),
            'world_guide': request.form.get('world_guide'),
            'genre': request.form.get('genre'),
            'tone': request.form.get('tone'),
            'style': request.form.get('style')
        }
        new_story = Story(**story_data)

        # --- World Generation ---
        # 1. Calculate number of entries
        length = new_story.target_length
        num_entries = 3 + math.floor(length / 1000) + math.floor(length / 10000)

        # 2. Generate initial world building topics (Phase 1 LLM call)
        prompt_phase1 = f"""
        Based on the following story idea, generate a list of {num_entries} world-building topics. For each topic, provide a category and a single, evocative sentence describing it.

        Story Prompt: {new_story.prompt}
        Main Character: {new_story.main_character_desc}
        World Guide: {new_story.world_guide}
        Genre/Tone: {new_story.genre}, {new_story.tone}

        Format your response as a numbered list. Each item should be a 'Category: Description'.
        Example:
        1. Magic System: A system based on celestial alignments, where power waxes and wanes with the moon.
        2. Political Structure: A council of five merchant guilds secretly controls the city-state from the shadows.
        """

        # For now, we'll just store the prompt. The generation will happen on the story page.
        # This is to provide a better user experience than a long wait on form submission.
        new_story.temp_prompt_phase1 = prompt_phase1 # Temporary attribute

        stories[new_story.id] = new_story

        return redirect(url_for('main_bp.story_page', story_id=new_story.id))

    """Renders the home page with the input form."""
    return render_template(
        'index.html',
        title='Story Generator',
        year=datetime.now().year,
    )

@main_bp.route('/story/<story_id>')
def story_page(story_id):
    """Displays the generated story components."""
    story = stories.get(story_id)
    if not story:
        abort(404)

    # This is where the generation would be triggered and results displayed.
    # For now, we'll just display the prompt that would be used.

    # A simple way to show progress would be to run generation steps here.
    # For this step, we'll run the world-building phase 1 prompt.
    if hasattr(story, 'temp_prompt_phase1') and not story.world_builder:
        initial_topics_text = generate_text(story.temp_prompt_phase1)

        # Parse the response and create WorldBuilderEntry objects
        entries = []
        for line in initial_topics_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue

            # Assuming format "N. Category: Description"
            parts = line.split(':', 1)
            if len(parts) == 2:
                # Clean up category part (remove numbering)
                category = parts[0].split('.', 1)[-1].strip()
                description = parts[1].strip()
                entries.append(WorldBuilderEntry(category=category, description=description))

        story.world_builder = entries
        del story.temp_prompt_phase1 # Clean up

        # --- World Generation Phase 2: Flesh out each entry ---
        for entry in story.world_builder:
            prompt_phase2 = f"""
            You are a creative world-building assistant. Take the following topic and expand it into a detailed, interesting paragraph. Then, provide exactly 4 comma-separated keywords relevant to the entry.

            Topic: {entry.category}
            Initial Idea: {entry.description}

            Format your response as follows:
            [Detailed paragraph]
            Keywords: keyword1, keyword2, keyword3, keyword4
            """

            # This can be slow as it calls the LLM for each entry.
            # In a real app, this would be a background job.
            full_entry_text = generate_text(prompt_phase2)

            # Parse the response
            try:
                description_part, keywords_part = full_entry_text.rsplit('Keywords:', 1)
                entry.description = description_part.strip()
                entry.keywords = [k.strip() for k in keywords_part.strip().split(',')]
            except ValueError:
                # If the format is not as expected, use the whole text as description
                entry.description = full_entry_text.strip()
                entry.keywords = []

    return render_template(
        'story.html',
        title="Your Story",
        year=datetime.now().year,
        story=story
    )
