# azerutils
Various small scale utilities and helper libraries for convenience purposes

## MultiStream / MultiSreamAcessor
Multistream is a thread safe wrapper for a stream like object which allows multiple readers to have independent read locations from the same underlying data stream.
Multistreams can be accessed directly by their "key" or through a MultiStreamAccessor which forwards a all calls to the underlying MultiStream with the appropriate key value.

To obtain a MultiStreamAccessor, use MultiStream.GetAccessor(_key) to get a copy of an existing stream, or MultiStream.GetNewAccessor() to generate a new stream.

## SpliceJsonHeader / \_\_jsonExtractIterator\_\_
SpliceJsonHeader takes a bytes stream-like object which begins with a JSON object and returns a string representing the JSON object. SpliceJsonHeader will read forward into the supplied stream for the length of the JSON object.

\_\_jsonExtractIterator\_\_ represents an iterator which expects a stream and iterates over stream counting the relative number of '{' and '}', stopping iteration when they are equal.