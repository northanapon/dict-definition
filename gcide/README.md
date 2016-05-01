# Entry Note
XML Structures of tags that we are interested in:

```xml
<entries>
  <entry key="..."> <!-- Word, always cap first letter -->
    <mhw source="...">...</mhw><!-- Ignore source "WordNet 1.5" -->
    <hw source="...">...</hw><!-- Ignore source "WordNet 1.5" -->
    <cs> <!-- Collocation segment -->
    	<col></col> <!-- Common combination -->
      	<mcol><col></col>...</mcol> <!-- sometimes,... -->
      	<fld></fld> <!-- Field, usually missing -->
      	<cd></cd>  <!-- Definition(s), sometimes missing -->
      	... <!-- continue in sequence -->
    </cs>
    <pos>...</pos><!-- Part of speech -->
    <plu><plw></plw></plu><!-- Plural form -->
    <vmorph><!-- Verb morphology -->
      <pos></pos>
      <conjf></conjf> <!-- Word -->
      ... <!-- continue in sequence -->
    </vmorph>
    <amorph><!-- Adjective morphology -->
      <pos>... &amp; ...</pos>
      <adjf></adjf> <!-- Word -->
      ... <!-- continue in sequence -->
    </amorph>
    <!-- There can be multiple def and fld in sequence
         or usually many sn -->
    <fld>...</fld><!-- Field -->
    <def><!-- Definition, usually missing if <sn> appears-->
      ... <!-- Definition text -->
      <as> <!-- Example, usually missing -->
        ... <ex></ex> ... <!-- Word usage -->
      </as>
      ...
      (<spn></spn> ... <spn></spn>) <!-- Species name, '(' and ')' indicates optional -->
      <mark></mark> See ... <!-- This is a rare case, but sometimes mark appears here and followed by "See ..." -->
    </def>
    <sn no="..."> <!-- Sense number -->
      <sd></sd><!-- Sub definition, similar to <sn> -->
      <fld></fld> <!-- Field of the sense -->
      <def></def> <!-- Definition, similar to entry.def-->
      <mark> ... &amp; ...</mark> <!-- A usage mark, some defs are bad -->
      <!-- mark
		- R: Rare
		- Obs: Obsolete
		- U. S: United States
		- Scot: Scotland, Scottish
		- Prov. Eng.: Provincial England
		- Colloq.: Colloquial
		- Archaic: very old
		- Mexico
		- Sp. Amer
		- Poetic
		- Colloq. U. S
		- Cant: Canticles?
		-->
    </sn>
   	<mark></mark>
  </entry>
</entries>
```
# GCIDE Definition Note
There are a few issues with GCIDE definition that we need to take care of.
So that the definition is *well-formed*. Here is the list of preprocessing:

- A definition is split into parts by `;` because each part is usually standalone.
- If there are many sentences in a part, only the first part is considered a definition
- A part that starts with `--`, `see`, `thus`, or `formerly` is removed.
- Conjunctive phrases staring the part including `also`, `hence`, `especially`, and `now commonly` are removed.
