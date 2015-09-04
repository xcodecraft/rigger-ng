<?php

class BooksSvc1 extends XSimpleService implements XService   //@REST_RULE: /books1/$uid,/books1/,/books1  
{}



//@REST_RULE: /books2
class BooksSvc2 extends XSimpleService implements XService   
{}


//@REST_RULE: /books3
class BooksSvc3 extends XSimpleService implements XService   {}



//@REST_RULE: /books4
//
class BooksSvc4 extends XSimpleService implements XService   {}



//@REST_RULE: /books5
//Hello
//
class BooksSvc5 extends XSimpleService implements XService   {}


//@REST_RULE: /books6
class BooksSvc6 extends XSimpleService    {}

//@REST_RULE: /books7
class BooksSvc7Bad extends XSimpleService    {}
class BooksSvc7 extends XSimpleService implements XService   {}
