
def add_css(content):
  HTML_WITH_CUSTOM_CSS = '''
    <!DOCTYPE html>
    <html>
    <head>

    <style>

    /*Import "PT Sans" */
    @import url(https://fonts.googleapis.com/css?family=PT+Sans:400,400italic,700,700italic);

    /*custom css for tables*/
    table a:link {{
      color: #666;
      font-weight: bold;
      text-decoration:none;
    }}
    table a:visited {{
      color: #999999;
      font-weight:bold;
      text-decoration:none;
    }}
    table a:active,
    table a:hover {{
      color: #bd5a35;
      text-decoration:underline;
    }}
    table {{
      font-family: "PT Sans", Helvetica, Arial, sans-serif;
      color: #515151;
      font-size: 0.8em;
      text-shadow: 1px 1px 0px #fff;
      background:#eaebec;
      margin:20px;
      border:#ccc 1px solid;

      -moz-border-radius:3px;
      -webkit-border-radius:3px;
      border-radius:3px;

      -moz-box-shadow: 0 1px 2px #d1d1d1;
      -webkit-box-shadow: 0 1px 2px #d1d1d1;
      box-shadow: 0 1px 2px #d1d1d1;
    }}
    table th {{
      padding:1em;
      border-top:1px solid #fafafa;
      border-left: 1px solid #fafafa;
      border-bottom:1px solid #e0e0e0;
      text-align: center;
      font-size: 120%;

      background: #b3cce6;
      background: -webkit-gradient(linear, left top, left bottom, from(#ededed), to(#ebebeb));
      background: -moz-linear-gradient(top,  #ededed,  #ebebeb);
    }}
    table th:first-child {{
      text-align: left;
      padding-left:20px;
    }}
    table tr:first-child th:first-child {{
      -moz-border-radius-topleft:3px;
      -webkit-border-top-left-radius:3px;
      border-top-left-radius:3px;
    }}
    table tr:first-child th:last-child {{
      -moz-border-radius-topright:3px;
      -webkit-border-top-right-radius:3px;
      border-top-right-radius:3px;
    }}
    table tr {{
      text-align: center;
      padding-left:20px;
    }}
    table td:first-child {{
      text-align: left;
      padding-left:20px;
      border-left: 0;
    }}
    table td {{
      padding:1em;
      border-top: 1px solid #ffffff;
      border-bottom:1px solid #e0e0e0;
      border-left: 1px solid #e0e0e0;

      background: #fafafa;
      background: -webkit-gradient(linear, left top, left bottom, from(#fbfbfb), to(#fafafa));
      background: -moz-linear-gradient(top,  #fbfbfb,  #fafafa);
    }}
    table tr.even td {{
      background: #f6f6f6;
      background: -webkit-gradient(linear, left top, left bottom, from(#f8f8f8), to(#f6f6f6));
      background: -moz-linear-gradient(top,  #f8f8f8,  #f6f6f6);
    }}
    table tr:last-child td {{
      border-bottom:0;
    }}
    table tr:last-child td:first-child {{
      -moz-border-radius-bottomleft:3px;
      -webkit-border-bottom-left-radius:3px;
      border-bottom-left-radius:3px;
    }}
    table tr:last-child td:last-child {{
      -moz-border-radius-bottomright:3px;
      -webkit-border-bottom-right-radius:3px;
      border-bottom-right-radius:3px;
    }}
    table tr:hover td {{
      background: #f2f2f2;
      background: -webkit-gradient(linear, left top, left bottom, from(#f2f2f2), to(#f0f0f0));
      background: -moz-linear-gradient(top,  #f2f2f2,  #f0f0f0);  
    }}
    </style>
    </head>
    <body>
    {content}
    </body>
    </html>
    '''

  return HTML_WITH_CUSTOM_CSS.format(content=content)
