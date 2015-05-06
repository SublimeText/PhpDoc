#PHPDoc

CodeDoc is a Sublime Text 2/3 plugin to speedup writing documenting comments.

Currently, [PhpDoc](http://phpdoc.org/) for PHP is supported, therefore CodeDoc is renamed to PhpDoc until support of other documentation types is added (if ever).

To use, just type in `/**` on the line right before class or function declaration, and then invoke auto-completion (with e.g. ctrl+space). This will get you a template for starters, with some values pre-filled on the fly (such as function arguments list). All common documenting keys are also available for manual input.

On some systems you have to fiddle a bit to find the auto-completion key. If it's not working on your system, just type `/**` and choose Edit->Show Completions. In the meny, in front of the item it will be the key combination for the auto-completion (e.g. ctrl+space, alt+/, etc)
