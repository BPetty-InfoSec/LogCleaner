# logcleaner.py

This is a tiny app to clean up log files and format them using RegEx.

Technically, this could be used with any type of text file for formatting.

The format files (you can have as many as you like) should live in the `formats`
directory. These files are json files, consisting of an array of objects. Each object
has two required attributes, and one semi-optional attribute. Each item in the file
will be run as a substitution against the selected log file sequentially.

## Format File Attributes

- `action`: This attribute determines what type of action this item will perform.
  - `delete`: This will substitute "" (nothing) for the `pattern` provided, effectively deleting all occurrences of the pattern
  - `replace`: This will substitute the `replace` attribute for `pattern` throughout the file
- `pattern`: This is the regEx pattern that will be matched against in the log file
- `replace`: This attribute is not required (and is ignored) for `delete` actions, but is necessary for for `replace` actions. The value of this attribute will be substituted for the `pattern` throughout the log file

## Sample Format File Structure

```json
[
    {
        "action": "delete",
        "pattern": " id=\"\\d+\""
    },
    {
        "action": "replace",
        "pattern": "<metadata>",
        "replace": "<!-- <metadata> -->"
    }
]
```
