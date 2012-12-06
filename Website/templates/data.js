/**
 * Created with PyCharm.
 * User: priya
 * Date: 12/3/12
 * Time: 10:25 PM
 * To change this template use File | Settings | File Templates.
 */

/* The data model for our Facet Browser is an array of JSON objects that represent your instances.
 * JSON, like XML, is incredibly easy to read and manipulate. You can easily add any properties you
 * like to an object. Unlike XML, JSON uses key value pairs to identify attributes. In the example
 * instances below, the properties are title, imageURL, description, facet1, facet2, facet3.
 *
 * Syntax
 *      {
 *          "key1":"value",
 *          "key2": ["value1", "value2"]
 *      }
 */


//exmaple data, you will replace these example instances with your own in Part 4 (remember to comment out or delete the example instances)

instances = [
    for tweet in tweets:
    {
        "title": "tweet",
        "facet1": "label"
    },
    {
        "title": "Tweet 1",

        "facet1": "Sports"
    },
    {
        "title": "Tweet 1",

        "facet1": "Entertainment"
    },
    {
        "title": "Tweet 1",

        "facet1": "Technology"
    },
    {
        "title": "Tweet 1",

        "facet1": "Sports"
    }

];
