# Profile

Profile and show an overview of what happens under the hood.

Profile is using [gprof2dot](https://github.com/jrfonseca/gprof2dot) by Jose Fonseca.

Required to have some visuale output is [DOT](http://www.graphviz.org/download/). 

Install DOT with [homebrew](https://brew.sh)  `brew install graphviz`

### Example

	from roboFontProfile import ShowProfile
	
	def myFunction():
		NewFont()
	
	ShowProfile(myFunction)


![image](profile.png)
