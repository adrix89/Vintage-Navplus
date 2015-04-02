import sublime, sublime_plugin

class move_to_regex(sublime_plugin.TextCommand):
	def run(self, edit,regex ="(?![[{()\]}\":',;]*$)[[{(,;\"'=]+[[{()\]}\"' *+,;]*(?!$)",expand=False,visual=True):
		v = self.view

		sels = v.sel()
		# print(sels)
		reg = []
		for sel in sels:
			if sel and visual:
				expand = True
			if expand:
				reg.append(sel.cover(v.find(regex, sel.end())))
			else :
				tmp = v.find(regex, sel.end())
				print("region temp= ",tmp.a)
				if tmp.a != -1:
					reg.append(tmp)
				else :
					reg.append(sel)
		sels.clear()
		p = 0
		if not expand:
			for sel in reg:
				sels.add(sublime.Region(sel.end()))
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
		# print("selection A=",sel.a," selevtion B=",sel.b)
		region= v.find("^[\t ]*", v.line(sel.b).begin() )
		if not sel:
			visual = False
		sels.clear()
		indent = region.size() + v.substr(region).count('\t')*(tab_width-1)
		indent2= indent
		change = False
		done  = False
		row,col = v.rowcol(region.begin())
		end_row = v.rowcol(v.size())[0]
		last_region = False
		if mode=="inside":
			if region.end() > sel.b:
				done = True
			else:
				for i in range(row+1,min( row+200,end_row+1)):
					region = v.find("^[\t ]*", v.text_point(i,0))
					indent2 = region.size()+ v.substr(region).count('\t')*(tab_width-1)
					if indent<indent2:
						done = True
						break
					elif indent>indent2:
						break
		elif mode=="outside":
			if region.end() < sel.b:
				done = True
			else:
				for i in range(row,max(row-200,0),-1 ):
					region = v.find("^[\t ]*", v.text_point(i-1,0))
					indent2 = region.size()+ v.substr(region).count('\t')*(tab_width-1)
					if indent>indent2 and v.line(region):
						done = True
						break
		elif mode=="forward":
			for i in range(row+1,min(row+200,end_row+1)):
				region = v.find("^[\t ]*", v.text_point(i,0))
				indent2 = region.size()+ v.substr(region).count('\t')*(tab_width-1)
				if indent2!=indent or not v.line(region) :
					change = True
					if last_region :
						region = last_region
						done = True
						break
				elif change and indent==indent2 and v.line(region):
					done = True
					break
				elif indent==indent2 and not change:
					last_region = region
		elif mode=="backward":
			for i in range(row,max(row-200,0),-1):
				region = v.find("^[\t ]*", v.text_point(i-1,0))
				indent2 = region.size()+ v.substr(region).count('\t')*(tab_width-1)
				if indent2!=indent or not v.line(region):
					change = True
					if last_region :
						region = last_region
						done = True
						break
				elif change and indent==indent2 and v.line(region):
					done = True
					break
				elif indent==indent2 and not change:
					last_region = region
		if visual and done:
			sels.add(sublime.Region(sel.begin(),sublime.Region(sel.b,v.line(region).end()).b) )
		elif done:
			sels.add(sublime.Region(region.end()))
		else:
			sels.add(sel)
		v.show(sels)

