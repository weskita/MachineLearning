from gensim.models import word2vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 # load up unzipped corpus from http://mattmahoney.net/dc/text8.zip
sentences = word2vec.Text8Corpus('../corpus/text8')
 # train the skip-gram model; default window=5
model = word2vec.Word2Vec(sentences, size=200)
 # ... and some hours later... just as advertised...
model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1) 
#[('queen', 0.5359965)]
 
 # pickle the entire model to disk, so we can load&resume training later
model.save('../models/text8.model')
 # store the learned weights, in a format the original C tool understands
model.save_word2vec_format('../models/text8.model.bin', binary=True)
 # or, import word weights created by the (faster) C word2vec
 # this way, you can switch between the C/Python toolkits easily