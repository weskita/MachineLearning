from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = word2vec.Word2Vec.load_word2vec_format('../models/text8.model.bin', binary=True)
# "boy" is to "father" as "girl" is to ...?
model.most_similar(['girl', 'father'], ['boy'], topn=3)
#[('mother', 0.61849487), ('wife', 0.57972813), ('daughter', 0.56296098)]
more_examples = ["he his she", "big bigger bad", "going went being", "big large small", "king men queen", "pig pork ox","woman man princess", "fish water you","france paris china","doctor medicine engineer","bed moonlight floor","red fire white"]
for example in more_examples:
     a, b, x = example.split()
     predicted = model.most_similar([x, b], [a])[0][0]
     print "'%s' is to '%s' as '%s' is to '%s'" % (a, b, x, predicted)

 
# which word doesn't go with the others?
model.doesnt_match("breakfast cereal dinner lunch".split())

print model.similarity('red','yellow')