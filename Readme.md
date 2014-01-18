MarvelLoad
==========

<pre>
usage:
	marvelload -c CONFIGFILE -db DBFILE COMMAND
		COMMANDS:
			init							Initializes the Database
			update							Fills the Database
			search term						Searches the Database for "term"
			list term						Lists all issues of the first series found by "term"
			download term issue [issue]		Download the issues for series found by term.
											Special: issue = all downloads all issues
</pre>
if no config is given, marvelload searches /etc/ and /home/USER/.config/ for a marvelload.conf.
See marvelload.conf.sample
