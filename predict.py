from keras.models import model_from_json
import datetime
from TweetSource import  *
import time

modeldir = "models/{}".format(datetime.date.today().isoformat())
with open('{}/model.json'.format(modeldir), 'r') as json_file:
    loaded_model_json = json_file.read()

loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights('{}/model.h5'.format(modeldir))
loaded_model.compile( optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])

words = TweetSource.load_json('{}/source.json'.format(modeldir))

while True:
    Y = loaded_model.predict(np.zeros((1,1,len(words))))
    tweet = []
    while True:
        choice = np.random.choice(words ,p=Y[0][0])
        if choice == '<EOT>' or len(tweet) == 50:
            print(' '.join(tweet))
            print()
            time.sleep(5)
            break
        elif choice != '<UNK>':
            tweet.append(choice)

        YA = np.zeros((1, 1, len(words)))
        YA[0,0,:] = to_categorical(words.index(choice), num_classes=len(words))
        Y = loaded_model.predict(YA)