from nltk.corpus import wordnet as wn

# Abstractness estimator based on WordNet
# abstractness = the mean of (#abstract_senses / #concrete_senses)
# Usage:
#    ae = AbstractnessEstimator()
#    ae.estimate('dog')
class AbstractnessEstimator:
    CONCRETE_NAME = 'physical_entity'
    ABSTRACT_NAME = 'abstraction'

    # Estimate the abstractness of a word
    # abstractness = the mean of (#abstract_senses / #concrete_senses)
    def estimate(self, word):
        # find lemmas whose surface is the same as a given word
        word = word.lower()
        lemmas = wn.lemmas(word, pos=wn.NOUN)
        abstractness_list = []
        for lemma in lemmas:
            # find all the hypernyms
            tree = lemma.synset.tree(lambda s:s.hypernyms())
            hypernyms = self._flatten(tree)

            # count physical_entity and abstraction synsets
            concrete = self._count_synset(hypernyms, self.CONCRETE_NAME)
            abstract = self._count_synset(hypernyms, self.ABSTRACT_NAME)
            # abstractness = #abst / (#abst + #conc)
            if (concrete + abstract) != 0:
                abstractness = float(abstract) / (abstract + concrete)
                abstractness_list.append(abstractness)

        # take the average (0 if no sense)
        if len(abstractness_list) != 0:
            result = sum(abstractness_list) / len(abstractness_list)
        else:
            result = 0.0
        return result

    # count the number of synsets that has a name
    def _count_synset(self, synsets, name):
        return len([s for s in synsets if s.name.startswith(name)])
    
    # flatten a list
    def _flatten(self, l):
        if isinstance(l, list):
            if l == []:
                return []
            else:
                return self._flatten(l[0]) + self._flatten(l[1:])
        else:
            return [l]

if __name__ == '__main__':
    print '=Usage example='
    print
    ae = AbstractnessEstimator()

    print 'Concrete examples'
    for word in ['dog', 'cat', 'cake']:
        print '', word, ae.estimate(word)

    print 'Semi-abstract examples'
    for word in ['spring', 'mountain', 'line']:
        print '', word, ae.estimate(word)

    print 'Abstract examples'
    for word in ['peace', 'justice', 'freedom']:
        print '', word, ae.estimate(word)

    print 'NOTE: unknown words are considered concrete'
    for word in ['hoge', 'dsfijf', '!!??']:
        print '', word, ae.estimate(word)
