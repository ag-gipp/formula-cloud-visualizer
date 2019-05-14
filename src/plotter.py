import matplotlib.pyplot as plt
import numpy as np
from expressions import *
import re
import matplotlib.ticker as tick
import matplotlib

plt.rc('text', usetex=True)
plt.rc('text.latex',
       preamble=r'\usepackage{amsmath} \usepackage{amssymb} ')

matplotlib.verbose.level = 'debug-annoying'

complexity = 5
alpha = 0.6
plotRange = [2000, 22000]
numResults = 20
lshift = 0.4
max = np.log(45000000)
min = np.log(10)

def y_fmt(tick_val, pos):
    if tick_val >= 1000000:
        val = int(tick_val)/1000000
        return '{:n}M'.format(val)
    elif tick_val >= 1000:
        val = int(tick_val)/1000
        return '{:n}k'.format(val)
    elif tick_val == 0:
        return '0'
    else:
        return int(tick_val)

filePath = "/opt/arxmliv/stats/allMMLDepth{:n}.txt".format(int(complexity))
file = open(filePath, "r")

freqs = []
labels = []

counter = 0
lineRegex = re.compile(r'^(\d+),(.*)$')

for line in file:
    if counter > numResults:
        break

    match = lineRegex.match(line)

    mml = match.group(2)
    if not mml or "span" in mml:
        continue

    print(mml)
    mml = "<math xmlns=\"http://www.w3.org/1998/Math/MathML\">" + mml + "</math>"
    latex = mathml2latex_yarosh(mml)
    print(latex)

    if "{,}_{2}" in latex:
        continue

    latex = re.sub(r'~', r'\sim', latex)
    latex = re.sub(r'\\ge\s', r'\\geq', latex)
    latex = re.sub(r'\u211d', r'\mathbb{R}', latex)
    latex = re.sub(r'\u210b', r'\mathcal{H}', latex)
    latex = re.sub(r'×', r'\\times ', latex)
    latex = re.sub(r'𝑑', r'd ', latex)
    latex = re.sub(r'𝐱', r'x ', latex)
    latex = re.sub(r'ℬ', r'\mathcal{B}', latex)

    latex = re.sub(r'\\left\(', r'(', latex)
    latex = re.sub(r'\\right\)', r')', latex)

    if "array" in latex:
        latex = r"$\left(\begin{smallmatrix}a& b\\ c& d\end{smallmatrix}\right)$"

    freq = int(match.group(1))
    freqs.append(freq)
    labels.append(latex)

    print(latex)
    counter += 1


x = range(len(freqs))
freqs.reverse()
labels.reverse()

cmap = matplotlib.cm.get_cmap('viridis')
normalize = matplotlib.colors.Normalize(
    vmin=min,
    vmax=max
)
colors = [cmap(normalize(np.log(value))) for value in freqs]

fig, ax = plt.subplots(figsize=(4, 8))
bars = ax.barh(x, freqs, align='center', color=colors)
ax.set_xlim(plotRange)
plt.xticks(fontsize=14)


ax.xaxis.set_major_formatter(tick.FuncFormatter(y_fmt))
plt.yticks(x, labels, rotation=0, fontsize=16)

counter = 0
tickLabels = ax.yaxis.get_ticklabels(which="both")
smallTextRegex = re.compile(r".*(int|sum|frac).*")

for label in tickLabels:
    label.set_verticalalignment('center')
    txt = label.get_text()
    if smallTextRegex.match(txt):
        label.set_fontsize(13)
    # depth 3
    # if counter == 12:
    #     label.set_position([-0.06, 0])
    # elif counter == 13:
    #     label.set_position([0.01, 0])
    # elif counter == 14:
    #     label.set_position([-0.04, 0])
    # depth 4
    # if counter == 8:
    #     label.set_position([-0.04, 0])
    # elif counter == 9:
    #     label.set_position([0.02, 0])
    # elif counter == 10:
    #     label.set_position([-0.03, 0])
    # elif counter == 18:
    #     label.set_position([-0.04, 0])
    # elif counter == 19:
    #     label.set_position([0.02, 0])
    # # depth 5
    # if counter == 0:
    #     label.set_position([0.02, 0])
    # elif counter == 2:
    #     label.set_position([-0.05, 0])
    # elif counter == 11:
    #     label.set_position([-0.04, 0])
    # elif counter == 17:
    #     label.set_position([-0.04, 0])
    # depth 6
    # if counter == 9:
    #     label.set_position([0, 0])
    # elif counter == 10:
    #     label.set_position([-0.04, 0])
    # elif counter == 11:
    #     label.set_position([0, 0])
    # elif counter == 12:
    #     label.set_position([-0.04, 0])
    # elif counter == 13:
    #     label.set_position([0, 0])
    # elif counter == 14:
    #     label.set_position([-0.04, 0])
    # elif counter == 15:
    #     label.set_position([0, 0])
    counter += 1

plt.margins(x=0.1, y=0.01)
plt.subplots_adjust(
    top = 0.96,
    bottom = 0.04,
    right = 0.95,
    left = lshift,
    hspace = 0,
    wspace = 0
)


beta = 0

zipY = range(0, len(freqs))
zipX = [(freqs[len(freqs)-1]+10)/(((rank+1) + beta)**alpha) for rank in zipY]

zipX.reverse()

labelTxt = "Zipf's Law\n$\\alpha = {:n}$".format(alpha)
ax.plot(zipX, zipY, '--', color='orange', label=labelTxt, linewidth=3)

plt.legend(loc="lower right", fontsize=14)

plt.title("Complexity {:n}".format(int(complexity)), fontsize=16, fontweight='bold')
# plt.show()
plt.savefig("../img/depth{:n}.svg".format(int(complexity)), format="svg", dpi=fig.dpi)
