# oelint.file.underscores

severity: error

## Example

``my_recipe_1.0.bb``

or

``my-recipe.bb``

## Why is this bad?

Bitbake's version detection takes the last chunk after a ``_`` of the filename as the default version.
If not present ``1.0`` is assumed, so any updates to the recipe might not result in a rebuild of the recipe.

## Ways to fix it

rename to

``my-recipe_1.0.bb``
