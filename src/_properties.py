PackageName = "Cheetah"
Title = "Cheetah: The Python-Powered Template Engine"
Description = "Provides Cheetah, a Python-powered template engine and code generator"
Status = 'Production'
Version = '0.9.10'
Maintainer = "Tavis Rudd"
Author = "The Cheetah Development Team"
AuthorEmail = "cheetahtemplate-discuss@lists.sf.net"
Url = "http://www.CheetahTemplate.org/"

Packages = ['%(PackageName)s',
            '%(PackageName)s.HelpDesk',
            '%(PackageName)s.HelpDesk.Docs',
            '%(PackageName)s.HelpDesk.Examples',
            '%(PackageName)s.Templates',
            '%(PackageName)s.Tests',
            '%(PackageName)s.Tools',
            '%(PackageName)s.Utils',                        
            ]
PackageDir = 'src'
PackageToDirMap = {'%(PackageName)s':'%(PackageDir)s',
                   '%(PackageName)s.HelpDesk.Docs':'docs',
                   '%(PackageName)s.HelpDesk.Examples':'examples',
                   }

Scripts = ['bin/cheetah-compile',
           ]

try:
    from Webware.Component import Component as _Component
    class ComponentClass(_Component):
        def _finalizeSettings(self):
            _Component._finalizeSettings(self)
            import os
            import os.path
            from distutils.core import Extension
            ## we only assume the presence of a c compiler on Posix systems, NT people will
            #  have to enable this manually. 
            if os.name == 'posix':
                extModules=[Extension("%(PackageName)s._namemapper" % self.settings(),
                                      [os.path.join("%(PackageDir)s" ,"_namemapper.c")
                                       % self.settings()
                                       ]
                                      )
                            ]
            else:
                extModules=[]
                
            self.setSetting('ExtModules', extModules )
except ImportError:
    pass
    