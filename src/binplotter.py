# libraries
import matplotlib.pyplot as plt
import numpy as np

input_file_path = "/opt/arxmliv/stats/rawFreqMini.txt"
freqs = [int(line.rstrip('\n')) for line in open(input_file_path)]

position = 1
ranks = range(1, len(freqs)+1)
# ranks = [position]
# prev_frq = freqs[0]
# for idx in range(1, len(freqs)):
#     if prev_frq == freqs[idx]:
#         ranks.append(position)
#     else:
#         position += 1
#         prev_frq = freqs[idx]
#         ranks.append(position)
#
# #x = [1/(idx + beta*x[idx]) for idx in range(0, len(x))]
#
# x = [np.log(f/sum(x)) for f in x] # norm and log of frequency
# y = [np.log(p) for p in y]

# Make the plot
# plt.hexbin(y, x, gridsize=(30, 30), cmap=plt.cm.get_cmap("BuGn"))
# plt.colorbar()
# plt.show()
#

margin = 0.7

fig = plt.figure(num=None, figsize=(6, 5.5))
plotter = fig.add_subplot(111)

plt.subplots_adjust(
    top = 0.92,
    bottom = 0.10,
    right = 1,
    left = 0.13,
    hspace = 0,
    wspace = 0
)

x = np.log(ranks)
y = np.log(freqs) - np.log(sum(freqs))
plotter.axis([x.min() - margin,
              x.max() + margin,
              y.min() - margin,
              y.max() + margin])

plotter.set_xlabel("$Log_e$ Frequency Rank")
plotter.set_ylabel("$Log_e$ Normalized Frequency")

hb = plotter.hexbin(x, y,
               gridsize=(20, 20),
               cmap='summer',
               reduce_C_function=np.sum,
               mincnt=1,    # minimum count per cell/bin
               bins='log',  # color scale is logarithmic for each bin
               alpha=0.7
)

fig.colorbar(hb)

# for all
# alpha = 1.3
# beta = 15.82

alpha = 1.33
beta = 15.82

zipX = range(1, len(ranks))
zipY = [1/((rank + beta)**alpha) for rank in zipX]

labelTxt = "Zipf's Law with $\\alpha = {:1.2f}$ and $\\beta = {:1.2f}$"\
    .format(alpha,beta)
plotter.plot(
    np.log(zipX),
    np.log(zipY),
    '--', color="orange",
    linewidth=2,
    label=labelTxt)
# plotter.plot(x, y, 'b')

plt.title("Top 3M Frequent Mathematical Expressions in arXiv", y=1.015)
plt.legend(loc="lower left")
plt.draw()

# plt.show()
plt.savefig("../img/all-first3M-zipf-comparison.svg", format="svg", dpi=fig.dpi)