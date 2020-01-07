# DHd2020

Skripte zum Beitrag:

Melanie Andresen, Anke Begerow, Lina Franken, Uta Gaidys, Gertraud Koch, Heike Zinsmeister (2020): 
Syntaktische Profile für Interpretationen jenseits der Textoberfläche.
DHd2020, Paderborn.

Das Skript ``collocations_surface.py`` berechnet die oberflächenbasierten Kollokationen, 
das Skript ``collocations_syntax`` die syntaxbasierten.
Das Skript ``llr.py`` ist nicht für den Beitrag entstanden, sondern stammt von Ted Dunning, siehe https://github.com/tdunning/python-llr.

Im Ordner ``demo-corpus`` werden Textdateien im conll-Format erwartet.
Die im Beitrag verwendeten Daten können aus Gründen des Datenschutzes bzw. des Urheberrechts nicht veröffentlicht werden.
Im Ordner ``demo-corpus`` befindet sich stattdessen eine geparste Version des [Foodblog-Korpus](https://zenodo.org/record/1410445).
Hierfür wurde der Parser [MATE](https://code.google.com/archive/p/mate-tools/wikis/ParserAndModels.wiki) (Bohnet 2010) 
mit einem auf der [Hamburg Dependency Treebank](http://hdl.handle.net/11022/0000-0000-7FC7-2) (Foth et al. 2014) trainierten Modell verwendet.

### Referenzen

Bohnet, Bernd. 2010. Very High Accuracy and Fast Dependency Parsing is not a Contradiction. 
Proceedings of the 23rd International Conference on Computational Linguistics (COLING 2010), 89–97. 
Beijing, China.

Foth, Kilian, Arne Köhn, Niels Beuck & Wolfgang Menzel. 2014. Because Size Does Matter: 
The Hamburg Dependency Treebank. Proceedings of LREC 2014, 2326-2333. Reykjavik, Iceland.
