from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, TimeDistributed, Activation, Masking
from TweetSource import  *
import datetime
import analyze

# summarize what was learned
print()
#print(tokenizer.document_count)
#print(tokenizer.word_index)
#print(tokenizer.word_docs)
# integer encode documents

vocabulary = 5000
batch_size = 32
min_tweet_length =10
epochs = 1
lstm = 500

cut = 98
total = 100
path = 'tweets/english_data_5000_10.json'

with open(path, 'r') as file:
    data = json.loads(''.join(file.readlines()));
    tweets = data['tweets']
    words = data['words']

trainT = [tweet for i,tweet in enumerate(tweets) if i%total<cut]
valT = [tweet for i,tweet in enumerate(tweets) if i%total>=cut]

trainS = TweetSource(trainT, words, batch_size=32)
valS = TweetSource(valT, words, batch_size=32)

model = Sequential()
model.add(Masking(mask_value=0, input_shape=(None, trainS.num_words)))
model.add(LSTM(lstm, return_sequences=True))
model.add(LSTM(lstm, return_sequences=True))
model.add(TimeDistributed(Dense(trainS.num_words)))
model.add(Activation('softmax'))
model.compile( optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])

model.fit_generator(trainS.generate_batches(),steps_per_epoch= trainS.tweet_count // batch_size,
                validation_data=valS.generate_batches(), validation_steps=valS.tweet_count // batch_size,
                    epochs=epochs,)

modeldir = "models/{}_{}_{}_{}".format(datetime.date.today().isoformat(),vocabulary, batch_size, min_tweet_length)
if not os.path.isdir(modeldir):
    os.mkdir(modeldir)

model_json = model.to_json()
with open('{}/model.json'.format(modeldir), "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("{}/model.h5".format(modeldir))
trainS.save_json("{}/source.json".format(modeldir))