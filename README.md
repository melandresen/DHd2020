# DHd2020

Skripte zum Beitrag:

Melanie Andresen, Anke Begerow, Lina Franken, Uta Gaidys, Gertraud Koch, Heike Zinsmeister (2020): 
Syntaktische Profile für Interpretationen jenseits der Textoberfläche.
DHd2020, Paderborn, Book of Abstracts. DOI: 10.5281/zenodo.3666690. S. 219–223.

Das Skript ``collocations_surface.py`` berechnet die oberflächenbasierten Kollokationen. 
Der Output besteht aus Wort_1, Wort_2, dem LLR-Wert und der absoluten Frequenz der Kombination (tabgetrennt).
Das Skript ``collocations_syntax`` berechnet die syntaxbasierten Kollokationen.
Der Output besteht aus Wort_1 (Dependent), der syntaktischen Relation zwischen den Wörtern, Wort_2 (Kopf), dem LLR-Wert und der absoluten Frequenz der Kombination (tabgetrennt).

Im Ordner ``demo-corpus`` werden Textdateien im Format CoNLL-X (2006) oder 2009 erwartet.
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
