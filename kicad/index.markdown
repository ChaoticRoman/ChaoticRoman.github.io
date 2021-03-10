<h1>KiCad</h1>
<a href="http://www.kicad-pcb.org">Homepage www.kicad-pcb.org</a><br>
<a href="https://launchpad.net/kicad">Code launchpad.net/kicad</a><br>
<p>

<h2>My python tools</h2>
<h3>My eeschema library</h3>

<a href="pyeeschema.tar">pyeeschema.tar</a><br>

<pre>
Archive contains:
pyeeschema/eeschema/schItem.py
pyeeschema/eeschema/sch.py
pyeeschema/eeschema/__init__.py
pyeeschema/setup.py

This is .sch python importer library, it has no dependence outside,
just pure python, I tried interface make clean, internals are bit
messy, but it is very short. It is made with some inspiration
from Mr. Baranovsky ans Svofski (klonor-kicad).

TODO:
- documentation
- cleanup
- s = Sheet() shouldn't contain any stuff after creation
- tests
</pre>

<h3>KiCad wxPython tools</h3>
<a href="hierarchicalKiCad.tar">hierarchicalKiCad.tar</a><br>

<pre>
hierarchicalKiCad/clone.py
hierarchicalKiCad/hierarchicalKiCad.py
hierarchicalKiCad/layClones.py
hierarchicalKiCad/refTools.py

It uses eeschema library above. hierarchicalKiCad.py is wxPython
utility to create high level schematics containng subsheets
copied from existing schematics. Program cares itself about,
references. existing schematics must have drawed rectangle
around content.

You can specify number of copies, the subschematics are copied,
modified and saved. I recommend new folder for this "build".

You must than normally contiune in eeschema: annotate, netlist.
Then goto pcbnew and import netlist. Then comes the time for
second utility.

TODO:
- documentation
- Restart reference numbering, right now is good to have every template
referenced from 1 (R1,R2,... etc.) to avoid high reference number buildup
- Bounding box automatical.

layClones.py is wxPython utility able to do board outline and layout
of clones from preceeding layouts. You need to provide high-level
schematic builded step before and board dimensions in mm. Template
layouts should have the same name.kicad_pcb and same path as original
template schematics, template pcb outline is specified by common
pcb edge outline.

pcbnew scripting inspired by LordBlick

TODO:
- Implement zones
- backup pristine (only netlist imported), it would need some consistency check
- backup already existing
</pre>

Test project <a href="test1.tar">test1.tar [4.6 MB]</a> contains template files
and directories "build1" and "build2" created by this utility. Try make yourself
build3 from files in root directory...

<p>

<a href="in_action.jpg"><img src="in_action.jpg"></a>

<h2>Compilation of latest KiCad version on Debian Testing</h2>

<h3>First time installation</h3>

Check if you have installed cmake>=2.8.1, zlib, wxGTK3 and wxGTK3-devel.

<pre>
bzr checkout lp:kicad
mkdir kicad/build
cd kicad/build
cmake -DBUILD_GITHUB_PLUGIN=ON  -DKICAD_SCRIPTING_WXPYTHON=ON -DKICAD_SCRIPTING=ON -DKICAD_SCRIPTING_MODULES=ON ../
make
make install
</pre>

For libraries of components and footprints do
<pre>
git clone https://github.com/KiCad/kicad-library.git
cd kicad-library
mkdir build 
cd build/ 
cmake ../ 
sudo make install
</pre>
Modules will be stored in /usr/local/share/kicad/modules.

Now if you want the KiCad documentation here you go:
<pre>
bzr branch --stacked lp:~kicad-developers/kicad/doc
cd kicad-doc
mkdir build 
cd build/ 
cmake ../
make
sudo make install
</pre>
Docs will be installed to /usr/local/share/doc/kicad/.

<h3>Update</h3>

<pre>
cd kicad/build
bzr update
make -j 2
make install
</pre>

Source: http://www.kicad-pcb.org/display/DEV/Building+KiCad+on+Linux
<p>

<h3>Significant  ~kicad-product-committers/kicad/product  revisions</h3>

<ul>
<li>5149 Forced wxWdigets>=3.0.0.
<li>3847 New format *.kicad_pcb instead of *.brd.
<ul>
