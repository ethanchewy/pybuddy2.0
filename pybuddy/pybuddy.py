"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import logging
import urllib
import json

from xblock.core import XBlock
from xblock.fields import Scope, String, Dict, Float, Boolean, Integer
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
#from .utils import _, DummyTranslationService, FeedbackMessage, FeedbackMessages, ItemStats, StateMigration, Constants
from pylint import lint
from astroid import MANAGER
from pylint.reporters.text import TextReporter
from subprocess import Popen, PIPE, STDOUT

LOG = logging.getLogger(__name__)
RESOURCE_LOADER = ResourceLoader(__name__)

class PythonBuddyXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    '''
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )
    '''

    #Set fields for teacher's to customize the problem
    #Instructor has to type &#10; for new line, &#009; for new tab
    data = String(
        display_name="Problem data",
        help=
            "Information about zones, items, feedback, and background image for this problem. "
            "This information is derived from the input that a course author provides via the interactive editor "
            "when configuring the problem."
        ,
        scope=Scope.content,
        default="asdfasdfasdfasdf",
    )


    max_attempts = Integer(
        display_name="Maximum attempts",
        help=
            "Defines the number of times a student can try to answer this problem. "
            "If the value is not set, infinite attempts are allowed."
        ,
        scope=Scope.settings,
        default=None,
    )

    question_text = String(
        display_name="Problem text",
        help="The description of the problem or instructions shown to the learner.",
        scope=Scope.settings,
        default="",
    )

    weight = Float(
        display_name="Problem Weight",
        help="Defines the number of points the problem is worth.",
        scope=Scope.settings,
        default=1,
    )

    attempts = Integer(
        help="Number of attempts learner used",
        scope=Scope.user_state,
        default=0
    )

    completed = Boolean(
        help="Indicates whether a learner has completed the problem at least once",
        scope=Scope.user_state,
        default=False,
    )

    grade = Float(
        help="Keeps maximum score achieved by student",
        scope=Scope.user_state,
        default=0
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def get_configuration(self):
        """
        Get the configuration data for the student_view.
        The configuration is all the settings defined by the author, except for correct answers
        and feedback.
        """



    # TO-DO: change this view to display your data your own way.
    def student_view(self, context):
        """
        The primary view of the PythonBuddyXBlock, shown to students
        when viewing courses.
        """
        '''
        html = self.resource_string("static/html/index.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/bootstrap.min.css"))
        frag.add_css(self.resource_string("static/css/style.css"))
        frag.add_css(self.resource_string("static/codemirror/lib/codemirror.css"))
        frag.add_css(self.resource_string("static/codemirror/lib/lint.css"))
        frag.add_css(self.resource_string("static/codemirror/addon/dialog.css"))

        frag.add_javascript(self.resource_string("static/js/jquery.js"))
        frag.add_javascript(self.resource_string("static/codemirror/lib/codemirror.js"))
        frag.add_javascript(self.resource_string("static/codemirror/lib/python.js"))
        frag.add_javascript(self.resource_string("static/codemirror/lib/lint.js"))
        frag.add_javascript(self.resource_string("static/js/cm-validator-remote.js"))
        frag.add_javascript(self.resource_string("static/codemirror/addon/search.js"))
        frag.add_javascript(self.resource_string("static/codemirror/addon/searchcursor.js"))
        frag.add_javascript(self.resource_string("static/codemirror/addon/dialog.js"))
        frag.add_javascript(self.resource_string("static/js/javascript.js"))
        frag.initialize_js('PythonBuddyXBlock')
        return frag
        '''
        context = {
            'fields': self.fields,
            'self': self,
            'data': urllib.quote(json.dumps(self.data)),
        }
        fragment = Fragment()
        fragment.add_content(RESOURCE_LOADER.render_template('public/html/index.html', context))
        css_urls = (
            'public/css/bootstrap.min.css',
            'public/css/style.css',
            'public/codemirror/lib/codemirror.css',
            'public/codemirror/lib/lint.css',
            'public/codemirror/addon/dialog.css'
        )
        #jquery might have errors since edx also loads jquery 
        js_urls = (
            #'public/js/jquery.js',
            'public/codemirror/lib/codemirror.js',
            'public/codemirror/lib/python.js',
            'public/codemirror/lib/lint.js',
            'public/js/cm-validator-remote.js',
            'public/codemirror/addon/search.js',
            'public/codemirror/addon/searchcursor.js',
            'public/codemirror/addon/dialog.js',
            'public/js/javascript.js'
        )
        for css_url in css_urls:
            fragment.add_css_url(self.runtime.local_resource_url(self, css_url))
        for js_url in js_urls:
            fragment.add_javascript_url(self.runtime.local_resource_url(self, js_url))

        fragment.initialize_js('PythonBuddyXBlock')
        return fragment
    def author_view(self, context):
        '''
        html = self.resource_string("static/html/index.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/bootstrap.min.css"))
        frag.add_css(self.resource_string("static/css/style.css"))
        frag.add_css(self.resource_string("static/codemirror/lib/codemirror.css"))
        frag.add_css(self.resource_string("static/codemirror/lib/lint.css"))
        frag.add_css(self.resource_string("static/codemirror/addon/dialog.css"))

        frag.add_javascript(self.resource_string("static/js/jquery.js"))
        frag.add_javascript(self.resource_string("static/codemirror/lib/codemirror.js"))
        frag.add_javascript(self.resource_string("static/codemirror/lib/python.js"))
        frag.add_javascript(self.resource_string("static/codemirror/lib/lint.js"))
        frag.add_javascript(self.resource_string("static/js/cm-validator-remote.js"))
        frag.add_javascript(self.resource_string("static/codemirror/addon/search.js"))
        frag.add_javascript(self.resource_string("static/codemirror/addon/searchcursor.js"))
        frag.add_javascript(self.resource_string("static/codemirror/addon/dialog.js"))
        frag.add_javascript(self.resource_string("static/js/javascript.js"))
        frag.initialize_js('PythonBuddyXBlock')
        return frag
        '''
        context = {
            'fields': self.fields,
            'self': self,
            'data': urllib.quote(json.dumps(self.data)),
        }
        fragment = Fragment()
        fragment.add_content(RESOURCE_LOADER.render_template('public/html/index.html', context))
        css_urls = (
            'public/css/bootstrap.min.css',
            'public/css/style.css',
            'public/codemirror/lib/codemirror.css',
            'public/codemirror/lib/lint.css',
            'public/codemirror/addon/dialog.css'
        )
        #jquery might have errors since edx also loads jquery 
        js_urls = (
            #'public/js/jquery.js',
            'public/codemirror/lib/codemirror.js',
            'public/codemirror/lib/python.js',
            'public/codemirror/lib/lint.js',
            'public/js/cm-validator-remote.js',
            'public/codemirror/addon/search.js',
            'public/codemirror/addon/searchcursor.js',
            'public/codemirror/addon/dialog.js',
            'public/js/javascript.js'
        )
        for css_url in css_urls:
            fragment.add_css_url(self.runtime.local_resource_url(self, css_url))
        for js_url in js_urls:
            fragment.add_javascript_url(self.runtime.local_resource_url(self, js_url))

        fragment.initialize_js('PythonBuddyXBlock')
        return fragment

    def studio_view(self, context):
        '''
        html = self.resource_string("static/html/index.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/bootstrap.min.css"))
        frag.add_css(self.resource_string("static/css/style.css"))
        frag.add_css(self.resource_string("static/codemirror/lib/codemirror.css"))
        frag.add_css(self.resource_string("static/codemirror/lib/lint.css"))
        frag.add_css(self.resource_string("static/codemirror/addon/dialog.css"))

        frag.add_javascript(self.resource_string("static/js/jquery.js"))
        frag.add_javascript(self.resource_string("static/codemirror/lib/codemirror.js"))
        frag.add_javascript(self.resource_string("static/codemirror/lib/python.js"))
        frag.add_javascript(self.resource_string("static/codemirror/lib/lint.js"))
        frag.add_javascript(self.resource_string("static/js/cm-validator-remote.js"))
        frag.add_javascript(self.resource_string("static/codemirror/addon/search.js"))
        frag.add_javascript(self.resource_string("static/codemirror/addon/searchcursor.js"))
        frag.add_javascript(self.resource_string("static/codemirror/addon/dialog.js"))
        frag.add_javascript(self.resource_string("static/js/javascript.js"))
        frag.initialize_js('PythonBuddyXBlock')
        return frag
        '''
        #Code based on xblock drag an drop by the edx-solutions team
        context = {
            'fields': self.fields,
            'self': self,
            'data': urllib.quote(json.dumps(self.data)),
        }
        fragment = Fragment()
        fragment.add_content(RESOURCE_LOADER.render_template('public/html/index.html', context))
        css_urls = (
            'public/css/bootstrap.min.css',
            'public/css/style.css',
            'public/codemirror/lib/codemirror.css',
            'public/codemirror/lib/lint.css',
            'public/codemirror/addon/dialog.css'
        )
        #jquery might have errors since edx also loads jquery 
        js_urls = (
            #'public/js/jquery.js',
            'public/codemirror/lib/codemirror.js',
            'public/codemirror/lib/python.js',
            'public/codemirror/lib/lint.js',
            'public/js/cm-validator-remote.js',
            'public/codemirror/addon/search.js',
            'public/codemirror/addon/searchcursor.js',
            'public/codemirror/addon/dialog.js',
            'public/js/javascript.js'
        )
        for css_url in css_urls:
            fragment.add_css_url(self.runtime.local_resource_url(self, css_url))
        for js_url in js_urls:
            fragment.add_javascript_url(self.runtime.local_resource_url(self, js_url))

        fragment.initialize_js('PythonBuddyXBlock')
        return fragment

    @XBlock.json_handler
    def check_code(self, data, suffix=''):
        print "hi123"
        #Get textarea text from AJAX call
        text = data['text']
        print "hello"

        #Open temp file which will be parsed

        #changed to w+ from r+ originally
        f = open("error_test.py","w+")
        f.seek(0)
        f.write(text)
        f.truncate()
        f.close()

        #Writable Object that will be used as a TextReporter
        class WritableObject(object):
            def __init__(self):
                self.content = []
            def write(self, st):
                self.content.append(st)
            def read(self):
                return self.content

        #Remember that you can configure with a seperate file for more specific limitations => --rcfile=/path/to/config.file . 
        #See http://stackoverflow.com/a/10138997/4698963
        #Add "--disable=R,C" to ARGs to print only errors & warnings
        ARGS = ["-r","n", "--disable=R,C","--msg-template={path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"]

        pylint_output = WritableObject()
        #Run Pylint, textreporter will redirect to writable object
        lint.Run(["error_test.py"]+ARGS, reporter=TextReporter(pylint_output), exit=False)
        pylint_list = pylint_output.content
        #Clear Cache. VERY IMPORTANT! This will make sure that there's no funky issues. See: http://stackoverflow.com/questions/2028268/invoking-pylint-programmatically#comment5393474_4803466 
        MANAGER.astroid_cache.clear()


        #Return json object, which is the pylint_output seperated by each newline
        return pylint_list

    #@XBlock.json_handler
    @XBlock.json_handler
    def run_code(self, data, suffix=''):
        print "run_test"

        #Remember file path depends on Operating System 
        cmd = 'python error_test.py'
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.read()

        return output

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("PythonBuddyXBlock",
             """<pybuddy data="for i in range(5):&#10;&#009;print i"
                max_attempts="3"/>
             """),
            ("Multiple PythonBuddyXBlock",
             """<vertical_demo>
                <pybuddy/>
                <pybuddy/>
                <pybuddy/>
                </vertical_demo>
             """),
        ]
