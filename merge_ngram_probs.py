import sys
import pickle

with open(sys.argv[1], 'rb') as f:
    data1 = pickle.load(f)
with open(sys.argv[2], 'rb') as f:
    data2 = pickle.load(f)

data_merged = {'prefix': {}, 'infix': {}, 'suffix': {}}
for _fix in ['prefix', 'infix', 'suffix']:
    changes, amount, maxdiff, maxdiff_ngram = 0, 0.0, 0.0, ''

    for ngram, prob in data1[_fix].items():
        data_merged[_fix][ngram] = prob
    for ngram, prob in data2[_fix].items():
        # data_merged[_fix][ngram] = (data_merged[_fix].get(ngram, prob) + prob) / 2
        if ngram not in data1[_fix] or prob == data1[_fix]:
            data_merged[_fix][ngram] = prob

        else: # if ngram in data1[_fix] and prob != data1[_fix][ngram]: 
            data_merged[_fix][ngram] = (data_merged[_fix][ngram] + prob) / 2

            # gather statistics of what changed
            changes += 1
            diff = abs(data1[_fix][ngram] - prob)
            amount += diff
            if diff > maxdiff:
                maxdiff = diff
                maxdiff_ngram = ngram + ' (' + str(data1[_fix][ngram]) + ' -> ' + str(prob) + ')'

    print('changes:', changes)
    print('amount:', amount)
    print('avg change:', amount / changes)
    print('maxdiff:', maxdiff)
    print('maxdiff_ngram:', maxdiff_ngram)

outfile = sys.argv[3] if len(sys.argv) > 3 else 'ngram_probs_merged.pickle'
with open(outfile, 'wb') as f:
    pickle.dump(data_merged, f, pickle.HIGHEST_PROTOCOL)
