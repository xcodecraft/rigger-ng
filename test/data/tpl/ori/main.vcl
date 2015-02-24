sub vcl_recv {

#%  T.host == '192.168.0.1' : {
    if (req.http.host ~ "%{HOST}" )
    {   
        set req.backend =  gstore_director ;
        unset req.http.Cookie ;
        if(req.request == "DELETE" || req.request == "PUT" ||  req.request == "POST" ) 
        {   

            if (req.url !~ "gameaccount" )
            {   
                ban( "req.http.host == "  + req.http.host +  " &&  req.url ~ " +  regsuball( regsuball(req.url,"\.","\.") , "\?.*",".*") ) ; 
            }   
        }   

    }   
#% }
#%  T.host == '127.0.0.1' : {
    if (req.http.host ~ "%{HOST}" )
    {   
        set req.backend =  gstore_director ;
        unset req.http.Cookie ;
        if(req.request == "DELETE" || req.request == "PUT" ||  req.request == "POST" ) 
        {   

            if (req.url !~ "gameaccount" )
            {   
                ban( "req.http.host == "  + req.http.host +  " &&  req.url ~ " +  regsuball( regsuball(req.url,"\.","\.") , "\?.*",".*") ) ; 
            }   
        }   

    }   
#% }
}
