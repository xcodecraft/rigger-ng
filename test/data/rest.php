<?php
class Action_main extends XAction
{
    public function _run($request,$xcontext)
    {
        return XNext::useTpl('index.html');
    }

}


class myres extends XSimpleRest implements XService
{
    public function get($request,$xcontext)
    {
        $xcontext->_result->success("get, hello world user: " . $request->uid);
    }
    public function set($request,$xcontext)
    {
        $xcontext->_result->error("set, post error", XErrCode::SYS_UNKNOW, 404);
    }
}

class game_his extends XSimpleService implements XService //@REST_RULE: /mygame/$uid/,/mygame/$uid
{
    public function _post($request,$xcontext)
    {
        XLogKit::logger("rest")->debug(__FUNCTION__,"his");
        XLogKit::logger("rest")->debug(__FUNCTION__);
        $xcontext->_result->error("post error",XErrCode::SYS_UNKNOW,404);
    }

    public function _put($request,$xcontext)
    {
        $xcontext->_result->error("put error");
    }
    public function _get($request,$xcontext)
    {
        $xcontext->_result->success("hellow world user: " . $request->uid );
    }
}

class friends extends XSimpleService implements XService        //@REST_RULE: /friends/$uid
{
    public function _post($request,$xcontext)
    {
        XLogKit::logger("rest")->debug(__FUNCTION__,"his");
        XLogKit::logger("rest")->debug(__FUNCTION__);
        $xcontext->_result->error("post error",XErrCode::SYS_UNKNOW,404);
    }

    public function _put($request,$xcontext)
    {
        $xcontext->_result->error("put error");
    }
    public function _get($request,$xcontext)
    {
        $xcontext->_result->success("hellow world user: " . $request->uid );
    }

}
