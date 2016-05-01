# WordNet Sense
We preprocess WordNet senses as follow:

- Senses referring to a person name is removed (lemma is capitalized) and lexical name is `noun.person`
- Definitions are split by `;` because each part is usually standalone.
- Self-referent parts are removed
- Starting context phrases (i.e. `(plural)`, or `physics`) are removed. For now...
- Quotation symbols are removed
- `To` is added to definitions of verbs. (To align with other dictionaries)
