#!/usr/bin/env python
import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import sys, os, re




XfwmColors = [
	"active_text_color", "inactive_text_color",
	"active_text_shadow_color", "inactive_text_shadow_color",
	"active_border_color", "inactive_border_color",
	"active_color_1", "active_color_2",
	"active_hilight_1", "active_hilight_2",
	"active_mid_1", "active_mid_2",
	"active_shadow_1", "active_shadow_2",
	"inactive_color_1", "inactive_color_2",
	"inactive_hilight_1", "inactive_hilight_2",
	"inactive_mid_1", "inactive_mid_2",
	"inactive_shadow_1", "inactive_shadow_2"
]


XfwmThings = {
	
	'menu'             : [ 'active', 'inactive', 'prelight', 'pressed' ],
	'hide'             : [ 'active', 'inactive', 'prelight', 'pressed' ],
	'shade'            : [ 'active', 'inactive', 'prelight', 'pressed' ],
	'shade-toggled'    : [ 'active', 'inactive', 'prelight', 'pressed' ],
	'stick'            : [ 'active', 'inactive', 'prelight', 'pressed' ],
	'stick-toggled'    : [ 'active', 'inactive', 'prelight', 'pressed' ],
	'maximize'         : [ 'active', 'inactive', 'prelight', 'pressed' ],
	'maximize-toggled' : [ 'active', 'inactive', 'prelight', 'pressed' ],
	'close'            : [ 'active', 'inactive', 'prelight', 'pressed' ],
	
	'top-left'     : [ 'active', 'inactive' ],
	'title-1'      : [ 'active', 'inactive' ],
	'title-2'      : [ 'active', 'inactive' ],
	'title-3'      : [ 'active', 'inactive' ],
	'title-4'      : [ 'active', 'inactive' ],
	'title-5'      : [ 'active', 'inactive' ],
	'top-right'    : [ 'active', 'inactive' ],
	'right'        : [ 'active', 'inactive' ],
	'bottom-right' : [ 'active', 'inactive' ],
	'bottom'       : [ 'active', 'inactive' ],
	'bottom-left'  : [ 'active', 'inactive' ],
	'left'         : [ 'active', 'inactive' ],
}


XfwmTypes = {
	
	"back-active"   : ( 'back', [ 'active', 'prelight', 'pressed' ] ),
	"back-inactive" : ( 'back', [ 'inactive'                      ] ),
	"fore-active"   : ( 'fore', [ 'active'                        ] ),
	"fore-lit"      : ( 'fore', [ 'prelight'                      ] ),
	"fore-pressed"  : ( 'fore', [ 'pressed'                       ] ),
	"fore-inactive" : ( 'fore', [ 'inactive'                      ] ),
	
}




EditableColors = {
	
	"back-active"   : { 'Symbol': "active_color_1"      , 'Color': '#123456' },
	"back-inactive" : { 'Symbol': "inactive_color_2"    , 'Color': '#888888' },
	"fore-active"   : { 'Symbol': "active_text_color"   , 'Color': '#FFFFFF' },
	"fore-lit"      : { 'Symbol': "active_hilight_1"    , 'Color': '#456789' },
	"fore-pressed"  : { 'Symbol': "active_shadow_1"     , 'Color': '#654321' },
	"fore-inactive" : { 'Symbol': "inactive_text_color" , 'Color': '#444444' },
	
}

ThemercColors = {
	'fore-active': 'active_text_color',
	'fore-inactive': 'inactive_text_color',
}




OwnDir = os.path.dirname(os.path.realpath(sys.argv[0]))




def Apply (name):
	
	asspath = OwnDir
	outpath = os.path.expanduser('~/.themes/' + name + '/xfwm4')
	
	try: os.makedirs(outpath)
	except: pass
	
	trcf = open(outpath + "/themerc", 'w')
	trcf.write('show_app_icon=true\n');
	
	for ci in ThemercColors:
		
		ec = EditableColors[ci]
		s = ThemercColors[ci]
		
		custom = ec['CustomSwitch'].get_active()
		color = StrHexRgba(ec['ColorBtn'].get_rgba())
		symbol = ec['ColorCombo'].get_active_text()
		
		if custom or symbol != s:
			trcf.write(s + '=' + (color if custom else symbol) + '\n')
	
	inames = [f for f in os.listdir(asspath) if '?' in f]
	
	for iname in inames:
		
		inf = open(asspath + "/" + iname)
		instr = inf.read()
		inf.close()
		
		pref = iname.split('-?')[0]
		states = XfwmThings[pref]
		
		for state in states:
			
			oname = pref + "-" + state + ".xpm"
			ostr = instr.replace('{name}', oname.replace('-', '_').replace('.', '_'))
			
			for eci in EditableColors:
				
				ci, ss = XfwmTypes[eci]
				
				if state in ss:
					
					ec = EditableColors[eci]
					
					custom = ec['CustomSwitch'].get_active()
					color = StrHexRgba(ec['ColorBtn'].get_rgba())
					symbol = ec['ColorCombo'].get_active_text()
					
					sym = '' if custom else ' s ' + symbol
					ostr = re.compile('\#.*\{' + ci + '\}').sub(color + sym, ostr)
			
			ouf = open(outpath + '/' + oname, 'w')
			ouf.write(ostr)
			ouf.close()
	
	trcf.close()
	
	def gett (arg = ''):
		return os.system('xfconf-query -c xfwm4 -p /general/theme ' + arg)
	def sett (name): gett('-s "' + name.replace('"', '\"') + '"')
	
	if name != gett(): sett('')
	sett(name)
	




W = Gtk.Window(title = "Plain")
W.set_position(Gtk.WindowPosition.CENTER)
W.set_icon_name('preferences-desktop-theme')
W.set_resizable(False)
W.set_border_width(8)
W.connect("destroy", lambda e: Gtk.main_quit())


CList = Gtk.Grid()
CList.set_row_spacing(4)
CList.set_column_spacing(4)
CList.Rows = []


def StrHexRgba (rgba):
	return '#{:02x}{:02x}{:02x}'.format (
		int(rgba.red * 0xFF + 0.5),
		int(rgba.green * 0xFF + 0.5),
		int(rgba.blue * 0xFF + 0.5)
	)


def UpdRow (rid):
	
	row = EditableColors[rid]
	custom = row['CustomSwitch'].get_active()
	
	row['ColorCombo'].set_sensitive(not custom)
	row['ColorBtn'].set_sensitive(custom)
	



def UpdName():
	
	tname = NameEntry.get_text()
	tpath = os.path.expanduser('~/.themes/' + tname)
	
	GoBtn.set_sensitive(tname)
	
	if tname and os.path.exists(tpath):
		NameEntry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, 'dialog-warning')
		NameEntry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, "Path exists!")
	else: NameEntry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)


for ti in sorted(XfwmTypes):
	
	t = XfwmTypes[ti]
	c = EditableColors[ti]
	
	nameLabel = Gtk.Label(' '.join([w.capitalize() for w in ti.split('-')]) + ':')
	colorBtn = Gtk.ColorButton(color = Gdk.color_parse(c['Color']))
	
	colorCombo = Gtk.ComboBoxText()
	for cid in XfwmColors: colorCombo.append_text(cid)
	colorCombo.set_active(XfwmColors.index(c['Symbol']));
	
	customSwitch = Gtk.Switch()
	customSwitch.set_tooltip_text("Custom color")
	
	CList.attach(nameLabel, 0, len(CList.Rows), 1, 1)
	CList.attach(colorCombo, 1, len(CList.Rows), 1, 1)
	CList.attach(customSwitch, 2, len(CList.Rows), 1, 1)
	CList.attach(colorBtn, 3, len(CList.Rows), 1, 1)
	
	c['ColorCombo'] = colorCombo
	c['CustomSwitch'] = customSwitch
	c['ColorBtn'] = colorBtn
	
	UpdRow(ti)
	customSwitch.connect("state-set", lambda s, e, ri = ti: UpdRow(ri))
	CList.Rows.append(c)

ThemeLabel = Gtk.Label("Name:")
NameEntry = Gtk.Entry()
GoBtn = Gtk.Button("Apply")

GoBtn.connect('pressed', lambda o: Apply(NameEntry.get_text()))
NameEntry.connect("changed", lambda e: UpdName());

CtlBox = Gtk.HBox(spacing = 8)
CtlBox.pack_start(ThemeLabel, True, True, 0)
CtlBox.pack_start(NameEntry, True, True, 0)
CtlBox.pack_start(GoBtn, True, True, 0)

All = Gtk.VBox(spacing = 8)
All.pack_start(CList, True, True, 0)
All.pack_start(CtlBox, True, True, 0)
W.add(All)

UpdName()

W.show_all()
Gtk.main()
