async function filterLocator(base_locator, filter_statement, page, logger) {
    const playwright_function = "(page.locator('" + base_locator + "').filter({" + filter_statement + "}))"
    logger("Filtering Playwright locator: " + playwright_function)
    const result = await eval(playwright_function);
    // If the result is an object we assume it's a locator so we return the _selector property of the locator object
    if (typeof result == "object") {
        return result._selector;
    } else {
        return result;
    }
}

filterLocator.rfdoc = `
This keyword returns a Playwright locator with the given filter applied.

Parameters:
base_locator : (string) The locator on which the filter should be applied.
filter_statement : (string) The filter to apply, e.g. 'hasText: "foo"'

Example
| Filter Locator  //li    hasText: "foo"
`

exports.__esModule = true;
exports.filterLocator = filterLocator;
