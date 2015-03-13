#开发指南

# 基础

### 依赖安装 

``` yaml
LibYAML install: http://pyyaml.org/download/libyaml/yaml-0.1.6.zip
./configure && make && make install
PyYAML install: http://pyyaml.org/download/pyyaml/PyYAML-3.11.zip
sudo python setup.py install
```
### 日志

``` python
from utls.rg_io import rg_logger

rg_logger.error()
rg_logger.info()
rg_logger.debug()
```

## 开发任务

### 测试用例

[示例](https://github.com/xcodecraft/rigger-ng/blob/master/test/res_tc/files_tc.py)

通过mock 对象获得res命令，然后与预期对比
``` python
        mock = base.tc_tools.res_mock()
        with   mock :
            impl.rg_run.run_cmd("conf,clean -s path -e dev",self.conf)

        expect= """
            if test ! -e ${PRJ_ROOT}/run/test_1; then   mkdir ....;
            if test ! -e ${PRJ_ROOT}/run/test_2; then   mkdir ....;
            if test -e ${PRJ_ROOT}/run/test_1 ; then rm -rf  ${PRJ_ROOT}/run/test_1 ; fi ;
            if test -e ${PRJ_ROOT}/run/test_2 ; then rm -rf  ${PRJ_ROOT}/run/test_2 ; fi ;
            """
        # print(mock.cmds)
        self.assertMacroEqual( expect, mock.cmds)
```

### 添加res

可以实现的接口
```python
  class controlable :
      def _before(self,context):
          pass
      def _after(self,context):
          pass
      def _start(self,context):
          pass
      def _stop(self,context):
          pass
      def _reload(self,context):
          pass
      def _config(self,context):
          pass
      def _data(self,context):
          pass
      def _check(self,context):
          pass
      def _clean(self,context):
          pass
      def _info(self,context):
          pass
```

继承于 
``` 
class path(interface.resource,shell_able):
        pass
```

[mysql 资源示例](https://github.com/xcodecraft/rigger-ng/blob/master/src/res/mysql.py)
