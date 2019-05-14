import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

from expressions import *

import matplotlib
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{amssymb}')
matplotlib.verbose.level = 'debug-annoying'

complexity = 1
comparison_level = 3
X = 0.4
Y = 0.8
max = 50

dataArxiv = "/opt/arxmliv/stats/allMMLDepth{:n}.txt".format(int(complexity))
dataZBM = "/opt/zbmath/stats/allMMLDepth{:n}.txt".format(int(complexity))

arxiv = open(dataArxiv, "r")
zbmath = open(dataZBM, 'r')

lineRegex = re.compile(r'^(\d+),(.*)$')

def loadFile(file):
    labels = []
    lineCounter = 0;
    for line in file:
        if lineCounter >= max:
            break
        match = lineRegex.match(line)
        mml = match.group(2)
        if not mml:
            labels.append("")
        elif "span" in mml:
            labels.append("$span))$")
        else:
            # print(mml)
            mml = "<math xmlns=\"http://www.w3.org/1998/Math/MathML\">" + mml + "</math>"
            latex = mathml2latex_yarosh(mml)
            # print(latex)

            # if "\\begin{array}{cc}a& b\\\\ c& d\\end{array}" in latex:
            #     latex = "$\\binom{a\\ b}{c\\ d}$"
            # elif "array" in latex:
            #     latex = ""
            # elif "$\\left({\\text{,}\\text{))[g]}\\right)}_{}$" in latex:
            #     latex = "$({\\text{,}\\text{))[g]})}_{}$"
            # elif "$\\underset{n\\to \\infty }{lim}$" in latex:
            #     latex = "$\lim_{n \\to \\infty}$"

            latex = re.sub(r'~', r'\sim', latex)
            latex = re.sub(r'\\ge\s', r'\\geq', latex)
            latex = re.sub(r'\u211d', r'\mathbb{R}', latex)
            latex = re.sub(r'\u210b', r'\mathcal{H}', latex)
            latex = re.sub(r'×', r'\\times ', latex)
            latex = re.sub(r'𝑑', r'd ', latex)
            latex = re.sub(r'𝐱', r'x ', latex)

            labels.append(latex)
            # print(latex)
        lineCounter += 1
    return labels

arxiv_labels = loadFile(arxiv)
zbmath_labels = loadFile(zbmath)

arxiv_ordered = []
zbmath_ordered = [-1 for i in arxiv_labels]

for aIDX, arxivLabel in enumerate(arxiv_labels):
    ahit = -1
    for zbIDX, zbl in enumerate(zbmath_labels):
        if zbl == arxivLabel:
            ahit = zbIDX
            zbmath_ordered[zbIDX] = aIDX
            break
    arxiv_ordered.append(ahit)


# draw line
# https://stackoverflow.com/questions/36470343/how-to-draw-a-line-with-matplotlib/36479941
def newline(p1, p2):
    ax = plt.gca()
    l = mlines.Line2D(
        [p1[0], p2[0]],
        [p1[1], p2[1]],
        color='green' if abs(p1[1]-p2[1]) < comparison_level else 'gray',
        marker='o',
        markersize=6,
        linestyle='solid' if abs(p1[1]-p2[1]) < comparison_level else 'dotted'
    )
    ax.add_line(l)
    return l


fig, ax = plt.subplots(1, 1, figsize=(6, 12), dpi=100)

# Vertical Lines
ax.vlines(x=X, ymin=1, ymax=max+0.5, color='black', alpha=0.7, linewidth=1, linestyles='dotted')
ax.vlines(x=Y, ymin=1, ymax=max+0.5, color='black', alpha=0.7, linewidth=1, linestyles='dotted')

# Points
# ax.scatter(y=df['1952'], x=np.repeat(1, df.shape[0]), s=10, color='black', alpha=0.7)
# ax.scatter(y=df['1957'], x=np.repeat(3, df.shape[0]), s=10, color='black', alpha=0.7)

# Line Segmentsand Annotation
# for p1, p2, c in zip(df['1952'], df['1957'], df['continent']):
#     newline([1,p1], [3,p2])
#     ax.text(1-0.05, p1, c + ', ' + str(round(p1)), horizontalalignment='right', verticalalignment='center', fontdict={'size':14})
#     ax.text(3+0.05, p2, c + ', ' + str(round(p2)), horizontalalignment='left', verticalalignment='center', fontdict={'size':14})

arxiv_range = np.arange(1, max+1, 1)
zbmath_range = np.arange(1, max+1, 1)
counter = 0

arxiv_labels.reverse()
zbmath_labels.reverse()

for c1, c2 in zip(arxiv_labels, zbmath_labels):
    otherHit = arxiv_ordered[counter]
    if otherHit >= 0:
        newline([X, max-counter], [Y, max-otherHit])
    else:
        plt.plot([X], [max-counter], marker='o', color='red')
    if zbmath_ordered[counter] < 0:
        plt.plot([Y], [max - counter], marker='o', color='red')
    ax.text(X-0.02, arxiv_range[counter], c1, horizontalalignment='right', verticalalignment='center', fontdict={'size':14})
    ax.text(Y+0.02, zbmath_range[counter], c2, horizontalalignment='left', verticalalignment='center', fontdict={'size':14})
    counter += 1

# 'Before' and 'After' Annotations
ax.text(X, max+1, 'ARXIV', horizontalalignment='center', verticalalignment='center', fontdict={'size':18, 'weight':700})
ax.text(Y, max+1, 'ZBMATH', horizontalalignment='center', verticalalignment='center', fontdict={'size':18, 'weight':700})

# Decoration
title = "Comparing Top 50 Frequent Math\nbetween arXiv and zbMATH with Complexity {:n}".format(complexity)

# ax.set_title(title, fontdict={'size': 22})

ax.set(xlim=(X-0.05, Y+0.05), ylim=(0.2, max+1.6))
ax.set_xticks([X, Y])
ax.set_xticklabels(["", ""])

yticks = np.arange(max, 0, -1)
plt.yticks(np.arange(1, max+1, 1), labels=yticks, fontsize=12)

# Lighten borders
plt.gca().spines["top"].set_alpha(.0)
plt.gca().spines["bottom"].set_alpha(.0)
plt.gca().spines["right"].set_alpha(.0)
plt.gca().spines["left"].set_alpha(.0)

plt.subplots_adjust(
    top = 0.99,
    bottom = 0,
    right = 0.97,
    left = 0.07,
    hspace = 0,
    wspace = 0
)

# plt.show()
plt.savefig("../img/comparisonDepth{:n}.svg".format(int(complexity)), format="svg", dpi=fig.dpi)