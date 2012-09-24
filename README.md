Log4j-Sublime
=============
Sublime plugin and syntax highlighting! Be gentle! Python amateur.

![](https://raw.github.com/scarrillo/Log4j-Sublime/master/imgs/log4j.png)

##### Quick Setup:
  1: Copy all files to:

      - OSX: /Users/_user_/Library/Application Support/Sublime Text 2/Packages/Log4j/
  
  2: Open: Log4j.tmTheme, copy the relevant theme 'dict' nodes to your current theme!


  3: Create and customize your key bindings:

    - Start log4j, specify a filter. Hint: debug
      { "keys": ["super+shift+t"], "command": "log4j" }

    - Bring the log4j panel to the front
      { "keys": ["ctrl+super+t"], "command": "show_panel", "args": {"panel": "output.log4j"} },


  4: Configure Log4j FileAppender. Example config, 'ConversionPattern' is important.

    log4j.appender.ToFile=org.apache.log4j.FileAppender
    log4j.appender.ToFile.threshold=DEBUG
    log4j.appender.ToFile.Append=false
    log4j.appender.ToFile.ImmediateFlush=true
    log4j.appender.ToFile.File=log4j.log
    log4j.appender.ToFile.layout=org.apache.log4j.PatternLayout
    log4j.appender.ToFile.layout.ConversionPattern=[%p][%c{2}]: %m%n

    - Expected output:
      [LEVEL][category]: Message

##### About the files:

  1: Log4j Syntax highlighting:

    - (compiled file) Log4j.tmLanguage
    - (source file) Log4j.JSON-tmLanguage

  2: Log4j Theme override definitions

    - Log4j.tmTheme

  3: Log4j Sublime Plugin scripts:

    - Log4j.py
    - tail.py
      ** This plugin requires Kasum's awesome Python tail script.
      ** His original code is here: https://github.com/kasun/python-tail
      It's bundled here as it has some small modifications that were required in order to stop it within a thread. Many thanks!

##### TODO:
  - Separate configuration for log file. Currently looks for: log4j.log
  - Regexp for filter
  - Optimize append. Has to be a cleaner way to open/configure/append this.
  - Figure out how to bundle this all up
  - Handle file resets gracefully
  - Learn more Python oO

  
