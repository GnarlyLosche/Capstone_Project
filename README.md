# Show Me The Money!! - Emotion Detection for Sales Call Performance - Capstone


![Looks like this call is going well!](https://github.com/GnarlyLosche/Capstone_Project/blob/main/Images/Zoom_Call_Predict.png)

When growing or building a business, the cost of onboarding can be immense. One of the first risks a company can run into is providing new hires with a poor onboarding experience, leading to less successful employees that can have a negative impact on the business' success. 

One area where this is all too common is on the sales team, especially with new business development Reps (BDRs), who usually have little to no past experience in sales. If your sales pipeline is less efficient due to poor training, not only will you generate less revenue, but the proportional expense of those new hires will increase.

Through this app managers can give the BDR insight into how their facial emotions likely appear to the prospect, and what the prospect’s likely emotion is at that point as well.

# Using This Notebook
Due to the number of images used (Over 65,000), If someone wants to recreate the models or use the notebooks, they must download the images through the links provided below in the Data Understanding section, and set up a project filepath as shown below.

Show Filepath Image Here

The final model uses an aggregated set of images for training, validation and testing. The breakdown of how the datasets were used for training, validation, and testing is:

**FER2013/AffectNet data split breakdown:**
- Training/Validation/Testing Split Ratio
    - 70% Training, 20% Validation, 10% Testing
    - Only AffectNet used for final testing set
- Change in size from initial model (only FER2013)
    - Training - 28,709
    - Updated Training - 48,197
    - Validation - 7,178
    - Updated Validation - 11,350 
    - New Unseen Testing - 4,163
- In order to train and validate the model effectively, there was an even 50/50 split between images from AffectNet and FER2013 for each emotion in both training and validation folder paths.


# Business Understanding

[According to Taskdrive.com](https://taskdrive.com/sales/sdr-cost-infographic/), **the average cost of hiring an in-house BDR team is around $6,000-$10,000 per SDR per month.** When you are paying that much per employee, it’s vital that they receive adequate training and feedback quickly so they can start generating revenue for your business.

Given the age of sales via video calls and demos, I built this tool to provide insight into the success of a sales team members during their meetings in order to help managers train effectively. 

I have worked iside of/developed a sales program at past startups, and I personally ran into issues as we scaled and our sales team grew without the adequate support it needed. My goal with this capstone and this project was to essentially design an MVP for a startup idea that could be used by other seed stage or Series A companies to prepare for growth.

Insight Partners is one of the worlds largest Venture Capital Firms in the world. One of the largest pitfalls they have identified in their portfolio companies when it comes to scaling and sales growth is hiring your sales team (and sales management) for industry experience instead of for sales experience ([Source](https://www.insightpartners.com/blog/hiring-a-sales-leader-part-i-5-common-pitfalls-to-avoid/)). 

Insight Identifies 5 Core Areas of a sales program than needs to develop for effective scaling:
1. Strong hiring practices and ability to coach and develop sales reps
2. Standardized sales processes and playbooks
3. Consistent pipeline management and forecasting calls
4. Stable and developing enablement programs
5. The appropriate infrastructure not only for today but also for the next 2-3 years

This tool was designed to help growing companies achieve both item one and two by providing a model designed to detect emotions on both the face of the sales staff and the prospect, and provide data-backed insight into how they are likely percieved by the prospect, and what that prospect is likely feeling at important moments in the sales script/pitch.

# Data Understanding

This project took data from two separate datasets in order to increase the size of available data to train the emotion detection model on and improve generalization on unseen data. 

## FER 2013
[Link to data](https://www.kaggle.com/datasets/msambare/fer2013?select=train)

![Example Images](https://production-media.paperswithcode.com/datasets/FER2013-0000001434-01251bb8_415HDzL.jpg)

Fer2013 contains approximately 30,000 facial RGB images of different expressions with size restricted to 48×48, and the main labels of it can be divided into 7 types: 0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral. The Disgust expression has the minimal number of images – 600, while other labels have nearly 5,000 samples each.
- FER2013 was used to build the inital model shown in Initial_Emotion_Detection_Model.ipnyb, but after developing the MVP the small size of the images (48x48) made me consider an additional dataset

## AffectNet HQ Subsample
[Link to data](https://www.kaggle.com/datasets/tom99763/affectnethq)

![Example Images](https://production-media.paperswithcode.com/datasets/AffectNet-0000001484-9dabde74_5sUXPfJ.jpg)

AffectNet is a large facial expression dataset with around 0.4 million images manually labeled for the presence of eight (neutral, happy, angry, sad, fear, surprise, disgust, contempt) facial expressions along with the intensity of valence and arousal.
- Since the initial model wasn't built to show the intensity of emotion, the AffectNet images were only used to classify emotions belonging to the emotions present in the FER2013 Dataset. As a result, the images labeled as showing contempt were ignored. 

# Modeling
## Baseline Model
In order to evaluate my model performance, I looked at the normalized value counts of the number of images under each emotion category in the combined AffectNet/FER2013 Train Dataset. 

If I were to build a model that always guessed the most frequent emotion (Happiness), my model would have a max accuracy of 22%

## Initial Model
My Initial Model was a Convolutional Neural Network trained using the FER2013 Dataset. My initial goal was to buil a model that would take in an image, and accurately predict the emotion show on the face in the image. To make this into a useful tool, I wanted the model to be able to generate an image that had the image, and the emotions overlaid onto the images in order to provide visuals a sales manager could use when they provide feedback to their sales team after their calls.

![Image of Train and Validation for Initial Model](https://github.com/GnarlyLosche/Capstone_Project/blob/main/Images/Initial_Model_V1.png)

Initially, my model was underfitting the data slightly. Given the level of accuracy and loss and the delta between each for train and validation, I decided to not worry about the underfitting.

One aspect I realized I forgot in my first model was that I didn't build out additional train and validation datasets to run the second model on (after applying weights)
- Initially, my transfer learning was re-applied to the same dataset, which could lead to worse generalization since it is reinforcing preconieved features (resulting from retraining on the same data)

![Inital Model Confusion Matrix](https://github.com/GnarlyLosche/Capstone_Project/blob/main/Images/Initial_Model_Matrix_V1.png)

Overall, my initial model had 56% Accuracy the below performance by emotion:

Emotion | Precision | Recall | F1
| :---: | :---: | :---: | :---:
angry | 0.43 | 0.50 | 0.46
disgust | 0.00 | 0.00 | 0.00
fear | 0.36 | 0.21 | 0.26
happy | 0.78 | 0.79 | 0.79
neutral | 0.49 | 0.62 | 0.55
sad | 0.45 | 0.41 | 0.43
surprise | 0.63 | 0.74 | 0.68

The poor performance on disgust was likely due to the size of the disgust-labeled data having a large class imbalanced compared to the other emotions. Inversely, the neutral and happy images were the largest labeled data sets. 

![Example prediction from first model vs actual labeled emotion](https://github.com/GnarlyLosche/Capstone_Project/blob/main/Images/Inital_Model_Probs.png)

Based on these results I looked for and found the AffectNet Dataset, hoping the increased number of images would improve overall model performance and address the class imbalance/performance on the disgust category.

## Final Model

![Model loss and performance before Transfer Learning](https://github.com/GnarlyLosche/Capstone_Project/blob/main/Images/Second_Model_before_TL_V1.png)

I planned on improving my detection model based on the FER2013 dataset, by adding an available subset of Images taken from the AffectNet dataset. Both sets of data have the same target label, which makes aggregating the images easier.

In doing so, I found that my model trains much, much slower. Likely due to the doubled size of the data, and the fact that the addition of the affectnet images meant more transformations had to be applied to the images during the train, validation, and test generator steps. Since transformations can only be applied using CPU power, it takes longer to run.

To address the reduction in speed I decided to use transfer learning to build an initial model that has very little data augmentation (CPU based transformations - model performance shown above) to get a strong initial model, and then build a second model that uses the ending weghts of that first version to further train on a second dataset that is much smaller, but has 3x the applied data augmentation steps.

Both models require data augmentation to rescale the AffectNet images, so CPU power will reduce learning rate given the size of the dataset. In order to avoid it slowing too much, I only using horizontal flip as an additional augmenting step at first. 

The model weights from this first model were used to build the final model, which had less images but more augmentation applied.

![Final Model Performance after Transfer Learning](https://github.com/GnarlyLosche/Capstone_Project/blob/main/Images/second_Model_After_TL.png)

![Confusion Matrix from final Model](https://github.com/GnarlyLosche/Capstone_Project/blob/main/Images/Second_Model_Matrix_V1.png)

With the creation of an unseen test set composed of exclusively AffectNet Images, I found that fear and disgust were completely ignored in my model's predictions on the test set. This may be due to the size of classified fear and disgust images in my training and validation datasets, but is indicative of a model that was not trained effectively. 

With that said, I am ok with poor performance on fear or disgust given the goal of the model. During sales calls, emotions like happiness, and anger are pivotal to classify. More than anything, the shift from neutral to happiness or anger is the indicator I care most about to indicate prospect interest or apathy.

# Final Model Evaluation

Emotion | Precision | Recall | F1
| :---: | :---: | :---: | :---:
angry | 0.40 | 0.74 | 0.52
disgust | 0.00 | 0.00 | 0.00
fear | 0.00 | 0.00 | 0.00
happy | 0.76 | 0.91 | 0.82
neutral | 0.56 | 0.83 | 0.67
sad | 0.50 | 0.38 | 0.43
surprise | 0.16 | 0.18 | 0.17

Overall, my final model has accuracy sitting at ~54% on the validation data, and on average 49% on the completely unseen test data. For most models and use cases, 50% accuracy is not high enough to be useful in a production environment.

Whith that said, my model baseline accuracy was 22%, so the model is much better than always guessing happiness as an emotion. This model is better than not using the model for emotion prediction.

# Considerations

Even humans are traditionally bad at predicting emotions based solely off of images. This model is based on label data from humans labelling emotions for people across all age ranges, races, and other demographics. A possible reason for my model accuracy is poor labeling, in addition to model training/data size. [Source:](https://www.nature.com/articles/d41586-020-00507-5)

As an example, below is an image of a baby from the AffectNet Dataset that was labeled as fearful that my model predicted as neutral. Qualitatively, I can understand why the person that labeled the image may have chosen fearful, but I could also justify neutral myself. **Note: The baby is blue because I used matplots image render to render the image in the notebook, which incorrectly showed the RGB values)**

![Image of Fearful Baby](https://github.com/GnarlyLosche/Capstone_Project/blob/main/Images/Baby_Fearful_1.png)

# Conclusion
When it comes to sales, there are key emotions that are important in understanding the level of interest you are getting from a prospect, but facial emotions alone will not tell you the whole story. [As mentioned on NPR](https://www.npr.org/2018/03/09/591875336/lisa-feldman-barrett-can-we-really-tell-how-other-people-are-feeling) humans find recognizing emotions solely off of facial expressions alone really difficult, because posture and body language are also indicators. My model may have a level of performance that is reflective of humanity's own ability to interpret emotions, instead of it's own poor performance. 

With more time there are a few things I would love to explore further:
- After applying the first run's model weights to train my final model, the validation loss and accuracy had much more noise - I would like to reduce the learning rate to reduce noise (run time is 19 hours - difficult to do in given time)
- Since my model used both datasets, I had to standardize my image sizes to 48x48 pixels, which helps improve processing speed, but may actually reduce performance. I would like to update my model to instead only use the AffectNet images, which are usually over 1000x1000 to see if there are micreoexpressions my model can use to increase performance.
- I know there are existing emotion detection models trained on much larger datasets (e.g. the enire AffectNet Dataset is over 1 million images) to see how my model performs compared to them
- My model is built using OpenCV's face detection model to find faces in images - my model is trained on images that may not necessarily have the same size or dimensions of the opencv bounding box, so I would like to look for additional face detection models to use.

