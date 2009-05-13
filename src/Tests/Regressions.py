#!/usr/bin/env python

import Cheetah.NameMapper 
import Cheetah.Template
import pdb

import unittest_local_copy as unittest # This is just stupid

class GetAttrException(Exception):
    pass

class CustomGetAttrClass(object):
    def __getattr__(self, name):
        raise GetAttrException('FAIL, %s' % name)

class GetAttrTest(unittest.TestCase):
    '''
        Test for an issue occurring when __getatttr__() raises an exception
        causing NameMapper to raise a NotFound exception
    '''
    def test_ValidException(self):
        o = CustomGetAttrClass()
        try:
            print o.attr
        except GetAttrException, e:
            # expected
            return
        except:
            self.fail('Invalid exception raised: %s' % e)
        self.fail('Should have had an exception raised')

    def test_NotFoundException(self):
        template = '''
            #def raiseme()
                $obj.attr
            #end def'''

        template = Cheetah.Template.Template.compile(template, compilerSettings={}, keepRefToGeneratedCode=True)
        template = template(searchList=[{'obj' : CustomGetAttrClass()}])
        assert template, 'We should have a valid template object by now'

        self.failUnlessRaises(GetAttrException, template.raiseme)


class InlineImportTest(unittest.TestCase):
    def test_FromFooImportThing(self):
        '''
            Verify that a bug introduced in v2.1.0 where an inline:
                #from module import class
            would result in the following code being generated:
                import class
        '''
        template = '''
            #def myfunction()
                #if True
                    #from os import path
                    #return 17
                    Hello!
                #end if
            #end def
        '''
        template = Cheetah.Template.Template.compile(template, compilerSettings={'useLegacyImportMode' : False}, keepRefToGeneratedCode=True)
        template = template(searchList=[{}])

        assert template, 'We should have a valid template object by now'

        rc = template.myfunction()
        assert rc == 17, (template, 'Didn\'t get a proper return value')

    def test_ImportFailModule(self):
        template = '''
            #try
                #import invalidmodule
            #except
                #set invalidmodule = dict(FOO='BAR!')
            #end try

            $invalidmodule.FOO
        '''
        template = Cheetah.Template.Template.compile(template, compilerSettings={'useLegacyImportMode' : False}, keepRefToGeneratedCode=True)
        template = template(searchList=[{}])

        assert template, 'We should have a valid template object by now'
        assert str(template), 'We weren\'t able to properly generate the result from the template'

    def test_ProperImportOfBadModule(self):
        template = '''
            #from invalid import fail
                
            This should totally $fail
        '''
        self.failUnlessRaises(ImportError, Cheetah.Template.Template.compile, template, compilerSettings={'useLegacyImportMode' : False}, keepRefToGeneratedCode=True)

    def test_AutoImporting(self):
        template = '''
            #extends FakeyTemplate

            Boo!
        '''
        self.failUnlessRaises(ImportError, Cheetah.Template.Template.compile, template)

    def test_StuffBeforeImport_Legacy(self):
        template = '''
###
### I like comments before import
###
#extends Foo
Bar
'''
        self.failUnlessRaises(ImportError, Cheetah.Template.Template.compile, template, compilerSettings={'useLegacyImportMode' : True}, keepRefToGeneratedCode=True)


class Mantis_Issue_11_Regression_Test(unittest.TestCase):
    ''' 
        Test case for bug outlined in Mantis issue #11:
            
        Output:
        Traceback (most recent call last):
          File "test.py", line 12, in <module>
            t.respond()
          File "DynamicallyCompiledCheetahTemplate.py", line 86, in respond
          File "/usr/lib64/python2.6/cgi.py", line 1035, in escape
            s = s.replace("&", "&") # Must be done first! 
    '''
    def test_FailingBehavior(self):
        import cgi
        template = Cheetah.Template.Template("$escape($request)", searchList=[{'escape' : cgi.escape, 'request' : 'foobar'}])
        assert template
        self.failUnlessRaises(AttributeError, template.respond)


    def test_FailingBehaviorWithSetting(self):
        import cgi
        template = Cheetah.Template.Template("$escape($request)", 
                searchList=[{'escape' : cgi.escape, 'request' : 'foobar'}], 
                compilerSettings={'prioritizeSearchListOverSelf' : True})
        assert template
        assert template.respond()


if __name__ == '__main__':
    unittest.main()
