vcl 4.0;
backend cn360 {
        .host = "www.360.cn";
        .port = "80";

    }

 sub vcl_recv {

     if (req.http.host ~ "www.360.cn" )
     {
         set req.backend_hint =  cn360 ;
         return (hash)  ;

     }
 }

