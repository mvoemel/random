<a name="readme-top"></a>

<!-- HERO SECTION -->
<div align="center">
  <h1 align="center">Random</h1>
  <p align="center">
    This repositories holds random projects, scripts, concepts, ect.
    <br />
    <a href="https://github.com/mvoemel/random/blob/main/moneymate">
        Moneymate
    </a>
    ·
    <a href="https://github.com/mvoemel/random/blob/main/algorithms">
        Algorithms
    </a>
    ·
    <a href="https://github.com/mvoemel/random/blob/main/theoretische-informatik">
        Theoretische Informatik
    </a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<ol>
  <li><a href="#moneymate">Moneymate</a></li>
  <li><a href="#chatroom">Chatroom</a></li>
  <li><a href="#blockchain">Blockchain</a></li>
  <li><a href="#algorithms">Algorithms</a></li>
  <li><a href="#python-scripts">Python Scripts</a></li>
  <li>
    <a href="#theoretische-informatik">Theoretische Informatik</a>
    <ul>
      <li><a href="#keller-automat">Keller Automat</a></li>
    </ul>
    <ul>
      <li><a href="#turing-maschine">Turing Maschine</a></li>
    </ul>
  </li>
  <li><a href="#license">Lizenz</a></li>
</ol>

![Java][Java]
![Python][Python]
![Javascript][Javascript]
![HTML][HTML]
![CSS][CSS]

## Moneymate

Money Mate is a user-friendly personal finance manager designed for young individuals, featuring an intuitive interface and a charming canine mascot to help users track income, expenses, and savings weekly. Developed by a team of four students as a school project, it involved meticulous planning, market research, and rigorous development, culminating in a successful presentation and valuable industry feedback.

<details>
  <summary>Detailed Description</summary>
  <p>Money Mate is a user-friendly personal finance manager for young individuals starting their independent lives. Featuring an intuitive interface and a charming canine mascot, it helps users track income, expenses, and savings weekly. Insightful charts visualize spending patterns, promoting better financial habits and informed decisions. Money Mate is a loyal companion in achieving financial wellness and independence.</p>
  <p>Money Mate began as a school project developed by our team of four students. We pitched the idea to investors, planned meticulously, and executed the development process. We conducted market research to understand the financial challenges faced by young individuals, designed a user-friendly interface, and incorporated a charming canine mascot. Through rigorous coding sessions and frequent meetings, we ensured each feature was functional and engaging. The project concluded with our presentation showcasing Money Mate's capabilities, receiving valuable feedback from industry experts, and marking a significant milestone in our educational journey.</p>
</details>

To learn more about this project visit the [README](/moneymate/README.md) page.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Chatroom

This small NodeJS project allows users realtime communication over a websocket. It showcases my understanding of websockets using the socket.io package.

To learn more about this project visit the [server.js](/chat-app/server.js) file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Blockchain

In this small Python project a Mini-Blockchain has been built.

To learn more about this project visit the [main.py](/blockchain/main.py) file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Algorithms

Up to this point in my career I have been exposed to several different problems in several different fields. For every set of problems there is a set of solutions. In the Algorithms folder I tried to save some of the algorithms I have been using. This spans from [Dynamic Programming](/algorithms/java/src/dynamicProgramming), over [Graph Theory](/algorithms/java/src/graphTheory) Algorithms to [Search and Sort](/algorithms/java/src/searchAndSort) Algorithms and [Parallel Computing](/algorithms/java/src/parallelProgramming) using several different Java Frameworks, ect.

<br/>

There is a [To-Be-Added](/algorithms/TBA.md) file with Algorithms and Concepts that might be added in the future.

<br/>

To learn more about this project visit the [Algorithms](/algorithms/) folder.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Python Scripts

Over the course of my programming journey I often had to use some python scripts to speed up some basic actions. This folder holds some of these scripts.

<br/>

To checkout some of my python scripts visit [Python Scripts](/python-scripts/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Theoretische Informatik

"Theoretische Informatik" was a module I had in my time at ZHAW. Once we had to design a Pushdown Automaton (Kellerautomat) with a UI and another time we had to programm a Turing Machine Emulator.

### Keller Automat

In this project I had to design a Pushdown Automaton with different functionalities, one of which is a "Step Mode" in which you can see (in a slow pace) how a Pushdown Automaton works.

I programmed it using **JavaScript** with **React** and **HTML** and **CSS**.

To learn more about this project visit [Keller Automat](/theoretische-informatik/keller-automat/).

### Turing Maschine

In this project I had to design a Turing Machine Emulator with different functionalities, one of which is the reading in of several different encodings for a "Universal Turing Maschine" (in form of binary, a long number, from a file, ect.). Another feature is the "Step Mode".

<details>
  <summary>Encoding</summary>

1. Schritt: Die Zustände Q einer TM werden codiert als:
   <br/>
   q1: für den Startzustand,
   <br/>
   q2: für den akzeptierenden Zustand (Jede TM mit mehreren akzeptierenden Zuständen kann in eine äquivalente TM mit
   nur einem akzeptierenden Zustand überführt werden.) und
   <br/>
   q3, . . . , qi : für alle weiteren Zustände.

2. Schritt: Die Bandsymbole Γ einer TM werden codiert als:
   <br/>
   X1: für das Symbol 0,
   <br/>
   X2: für das Symbol 1,
   <br/>
   X3: für das Symbol ␣ (Blank) und
   <br/>
   X4, . . . , Xj : für alle weiteren Symbole.

3. Schritt: Codierung der Richtung des Lese-Schreibkopfes D einer TM:
   <br/>
   D1: für die Richtung L und
   <br/>
   D2: für die Richtung R.

4. Schritt: Repräsentation einer Übergangsfunktion δ einer TM:
   <br/>
   Ein Übergang δ(qi, Xj) = (qk, Xl, Dm) einer TM wird codiert überdie Zeichenreihe:
   <br/>
   0^i10^j10^k10^l10^m mit (i, j, k, l, m ∈ N)

5. Schritt: Zusammenfassung der Übergangsfunktion δ einer TM:
<br/>
Die einzelnen Transitionen werden durch „11“ voneinander getrennt (jedes Ci steht für eine Transition):
<br/>
C111C211C311 . . .
</details>

I programmed it using the "Object oriented Pattern" with **Python**.

To learn more about this project visit [Turing Machine](/theoretische-informatik/turing-maschine/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

[MIT License](/LICENSE)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Java]: https://img.shields.io/badge/java-%23ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Javascript]: https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E
[HTML]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[CSS]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white
