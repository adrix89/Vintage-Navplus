import sublime, sublime_plugin

class move_to_regex(sublime_plugin.TextCommand):
	def run(self, edit,regex ="(?![[{()\]}\":',;]*$)[[{(,;\"'=]+[[{()\]}\"' *+,;]*(?!$)",end=True,expand=False,visual=True):
		v = self.view
		sels = v.sel()
		# print(sels)
		reg = []
		for sel in sels:
			if sel and visual:
				expand = True
				reg.append(sel.cover(v.find(regex, sel.end())))
			else :
				reg.append(v.find(regex, sel.end()))
		sels.clear()
		p = 0
		if not expand:
			if end:
				for sel in reg:
					sels.add(sublime.Region(sel.end()))
					p = sel.end()
			else:
				for sel in reg:
					sels.add(sublime.Region(sel.begin()))
					p = sel.end()
		else:
			for sel in reg:
				sels.add(sel)
				p = sel.end()
		v.show(p)



class move_to_indent(sublime_plugin.TextCommand):
	def run(self, edit,mode="inside",visual=False):
		v = self.view
		tab_width = v.settings().get("tab_size")
		sels =  v.sel()
		sel = sels[0]
		mark = sel.a
		go = sel.b
		print("selection A=",sel.a," selevtion B=",sel.b)
		if mode=="inside" or mode=="forward":
			region= v.find("^[\t ]*", v.line(go).begin() )
		else :
			region= v.find("^[\t ]*", v.line(go).begin() )
		if not sel:
			visual = False
		sels.clear()
		indent = region.size() + v.substr(region).count('\t')*(tab_width-1)
		indent2= indent
		change = False
		done  = False
		row = v.rowcol(region.begin())[0]
		end_row = v.rowcol(v.size())[0]
		if mode=="inside":
			for i in range(row+1,min( row+200,end_row )):
				region = v.find("^[\t ]*", v.text_point(i,0))
				indent2 = region.size()+ v.substr(region).count('\t')*(tab_width-1)
				if indent<indent2:
					done = True
					break
		elif mode=="outside":
			for i in range(row,max(row-200,0),-1 ):
				region = v.find("^[\t ]*", v.text_point(i-1,0))
				indent2 = region.size()+ v.substr(region).count('\t')*(tab_width-1)
				if indent>indent2 and v.line(region):
					done = True
					break
		elif mode=="forward":
			for i in range(row+1,min(row+200,end_row)):
				region = v.find("^[\t ]*", v.text_point(i,0))
				indent2 = region.size()+ v.substr(region).count('\t')*(tab_width-1)
				if indent2!=indent or not v.line(region) :
					change = True
				elif change and indent==indent2 and v.line(region):
					done = True
					break
		elif mode=="backward":
			for i in range(row-1,max(row-200,0),-1):
				region = v.find("^[\t ]*", v.text_point(i-1,0))
				indent2 = region.size()+ v.substr(region).count('\t')*(tab_width-1)
				if indent2!=indent or not v.line(region):
					change = True
				elif change and indent==indent2 and v.line(region):
					done = True
					break
		if visual and done:
			sels.add(sublime.Region(sel.begin(),sublime.Region(sel.b,v.line(region).end()).b) )
		elif done:
			sels.add(sublime.Region(region.end()))
		else:
			sels.add(sel)
		v.show(sels)

class last_com(sublime_plugin.TextCommand):
	def run(self, edit):
		i = 0
		history = self.view.command_history(i, True)
		
		while (history[0] == 'last_com' and history[0] is not None):
			history = self.view.command_history(i)
			i -= 1
		print(history)
		if history[0] is not None:
			self.view.run_command(history[0],history[1])