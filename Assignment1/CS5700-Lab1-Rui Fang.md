## CS5700-Lab1-Rui Fang

### Step 1: Manual GET with Telnet

![](/Users/Rui/Desktop/Screen Shot 2018-09-30 at 20.39.53.png)

1. What version of HTTP: HTTP/1.1

2. How is the beginning of the content sent by the server recognized by the client?

   - An empty line marks the end of content


   - Header and body has an empty line. This empty line tells client below is body.
   - Header has "Content-Length: 33997", this length tells client how long the body is. 

   Through this two steps the client recognize the content.

3. How does the client know what type of content is returned?

   The header has a "Content-Type". Here is text/html.

### Step 2: Capture a Trace

![](/Users/Rui/Desktop/Screen Shot 2018-09-30 at 21.09.01.png)

### Step 3: Inspect the Trace

![](/Users/Rui/Desktop/Screen Shot 2018-09-30 at 21.17.08.png)

1. What is the format of a header line?

   The format of a header line is like a key-value pair. For example: Content-Type: image/gif\r\n.

2. What headers are used to indicate the kind and length of content that is returned in a response?

   - Kind of content: Content-Type
   - Length: Content-Length

### Step 4: Content Caching

1. If-Modified-Since
2. The timestamp comes from Last-Modified