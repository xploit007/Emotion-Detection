# Emotion Detection in Tweets - Multi-label Classification

This project focuses on detecting multiple emotions in tweets using a multi-label classification model. The model uses a custom `Trainer` class from Hugging Face, with PyTorch for training. It also incorporates handling of class imbalance by computing positive weights for each emotion label. Custom tokens are created for specific cases like hashtags or slang to improve performance.

## Overview

- **Problem**: Classify tweets into multiple emotions, such as anger, joy, sadness, and more. Each tweet may be associated with multiple emotions simultaneously.
- **Solution**: A multi-label classification model built with Hugging Face and PyTorch.
- **Custom Tokenization**: For certain tokens (e.g., hashtags, slang), custom tokens are created to improve understanding of tweet patterns.

### Key Features:
- **Multi-label Classification**: Tweets can contain more than one emotion label.
- **Class Imbalance Handling**: Positive weights are computed for each emotion to address class imbalances.
- **Custom Token Creation**: Special handling for unique tokens (e.g., hashtags) to improve model performance.
- **Integration with Hugging Face**: Fine-tuning and training are done using Hugging Face models and tokenizers.
- **Integration with wandb**: Track experiments and metrics using Weights & Biases for model monitoring and visualization.

## Usage

1. **Set Up Tokens**:
   - **Hugging Face Token**: If you're using Hugging Face models, you'll need to authenticate using your Hugging Face token. Create a `.env` file and add your token like this:
     ```
     HF_TOKEN=<your_hugging_face_token>
     ```
   - **wandb Token**: To track experiments on Weights & Biases, you also need to set up your `wandb` token:
     ```
     WANDB_API_KEY=<your_wandb_token>
     ```

2. **Run the Notebook**: 
   - The notebook starts by importing necessary libraries and loading the dataset. 
   - Follow the instructions in the notebook to tokenize the data, calculate positive weights, and set up the custom `Trainer`.

## Model and Training

- **Custom Trainer**: The model uses a custom `Trainer` class to calculate binary cross-entropy loss with class weights. The positive weights for each emotion label are computed dynamically based on label frequencies.
- **Tokenization**: Custom tokens are created for handling unique patterns in the text, such as hashtags, mentions, and emoticons.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

