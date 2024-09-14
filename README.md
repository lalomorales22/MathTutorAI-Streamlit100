# Math Tutor AI: Personalized Math Problem Solving Assistance

Math Tutor AI is a Streamlit-based web application that provides personalized assistance in solving math problems across different levels. This AI-powered tutor uses various language models to offer step-by-step explanations, guidance, and solutions to mathematical problems.

## Features

- Interactive chat interface for asking math questions and describing problems
- Support for multiple AI models, including OpenAI's GPT models and Ollama's local models
- Customizable focus on specific math categories
- Adjustable difficulty levels (Elementary to Graduate)
- Dark/Light theme toggle
- Conversation saving and loading functionality
- Token usage tracking

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/lalomorales22/MathTutorAI-Streamlit100.git
   cd math-tutor-ai
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

4. (Optional) If you want to use Ollama models, make sure you have Ollama installed and running on your system.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run math_tutor_ai.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter your name, select your preferred math categories and difficulty level, and start asking math questions!

## Customization

- You can modify the `MATH_CATEGORIES` and `DIFFICULTY_LEVELS` lists in the code to add or remove categories and levels.
- The custom instructions for the AI can be adjusted in the sidebar of the application.

## Contributing

Contributions to improve Math Tutor AI are welcome! Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
