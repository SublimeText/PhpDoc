import sublime, sublime_plugin
import os, re

syntax_list = {
	"PHP": True
}

class CodedocCommand(sublime_plugin.TextCommand):
	def write(self, view, str):
		view.run_command('insert_snippet', {
			'contents': str
		})

	def run(self, edit, insert=None):
		v = self.view
		if insert == "newline":
			self.write(v, "\n* ")
		elif insert == "newline-first":
			self.write(v, "\n * ")

class CodedocEv(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		# only complete single line/selection
		if len(locations) != 1:
			return []

		# check is supported type of file
		syntax, _ = os.path.splitext(os.path.basename(view.settings().get('syntax')))
		syntax = syntax_list.get(syntax)
		if syntax == None:
			return []

		if view.substr(sublime.Region(view.line(locations[0]).a, locations[0])).find("/**") == -1:
			return []

		# find end of completion line
		currLineEnd = view.find('[\n\r]', locations[0])
		if currLineEnd is None:
			return []

		# find end of function/class declaration (php delimiter)
		nextLineEnd = view.find('[{;]', currLineEnd.end())
		if nextLineEnd is None:
			return []

		declaration = view.substr(sublime.Region(currLineEnd.end(), nextLineEnd.begin()))
		if declaration.find("function") > -1:
			snippet = self.expandPhpFunction(declaration)
			if snippet:
				return [('/**', snippet)]
		elif (declaration.find("class") > -1 or declaration.find("interface") > -1 or declaration.find("trait") > -1):
			snippet = self.expandPhpClass(declaration)
			if snippet:
				return [('/**', snippet)]
		elif (declaration.find("public") > -1 or declaration.find("private") > -1 or declaration.find("protected") > -1) and declaration.find("$") > -1:
			snippet = self.expandPhpVar(declaration)
			if snippet:
				return [('/**', snippet)]

		return []

	def expandPhpClass(self, declaration):
		snippet = '/**\n'
		snippet += ' * ${1}\n'
		snippet += ' */'
		return snippet

	def expandPhpVar(self, declaration):
		snippet = '/**\n'
		snippet += ' * @var ${1:type}\n'
		snippet += ' */'
		return snippet

	def expandPhpFunction(self, declaration):
		rex = re.compile("\((.*)\)", re.DOTALL)
		m = rex.search(declaration)
		if not m:
			return None
		params = m.group(1).split(',')

		snippet = '/**\n * ${1:Description}\n'

		i = 2
		for p in params:
			defval = ''
			p2 = p.find('=')
			if p2 > -1:
				dval = p[p2+1:].lower().strip()
				if dval == 'true' or dval == 'false':
					defval = 'bool'
				elif dval == 'null':
					defval = 'null'
				elif dval.find('array(') == 0 or dval[0] == '[':
					defval = 'array'
				elif dval[0] == '"' or dval[0] == '\'':
					defval = 'string'

				if defval == '':
					rex = re.compile("^[0-9].+")
					m = rex.search(dval)
					if m:
						defval = 'int'
				elif defval == '':
					defval = dval;

				p = p[0: p2]

			p = p.strip()

			p = p.replace('$', '\$')
			if p == '':
				continue

			p3 = p.find(' ')
			if p3 > -1:
				type = p[0:p3] + ('|' if defval != '' else '')
				p = p[p3+1:].strip()
			else:
				type = '${' + str(i) + ':type' + ('|' if defval != '' else '')  + '}'


			snippet += ' * @param ' + type + defval + ' ' + p + ' ${' + str(i + 1) + '}\n'
			i += 2

		snippet += ' * @return ${' + str(i) + ':type}\n'
		snippet += ' */'
		return snippet
