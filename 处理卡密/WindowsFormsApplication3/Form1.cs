using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

using System.Windows.Forms;

namespace WindowsFormsApplication3
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string input = richTextBox1.Text.Trim();
            //string pattern = @"[0-9]{19}";
            string pattern = @"(?<=张)\d{2,3}(?=元充值卡)|[0-9]{19}";
            Regex regex = new Regex(pattern);
            var arr = regex.Matches(input).Cast<Match>().ToArray();
            richTextBox1.Clear();

            string sn2 = DateTime.Now.Year.ToString().Substring(2, 2) + DateTime.Now.ToString("MMddHHmm");
            Dictionary<string, List<string>> dict1 = new Dictionary<string, List<string>>();
            var lst = new List<string>();
            string key = "";
            foreach (var i in arr)
            {
                if (i.Value.Length < 4)
                {
                    
                    if (!dict1.ContainsKey(i.Value))
                    {
                        dict1.Add(i.Value, new List<string>());
                    }
                    key = i.Value;
                    lst = dict1[i.Value];
                }
                else
                {
                    lst.Add(i.Value);           
                }
                     }
            foreach (var j in dict1.Keys)
            {
                richTextBox1.Clear();
                lst = dict1[j];
               string sn = j.Substring(0, 2) + sn2 + "001";
                long a = long.Parse(sn);
                int i = 0;
                foreach (string rows in lst)
                {
                    i++;
                    sn=a.ToString();
                    a++;
                    richTextBox1.Text += sn + "\t" + rows + "\t" + j + ".00" + Environment.NewLine;
                }
                string dk = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
                richTextBox1.SaveFile(dk + "\\130" + j + "mini-" + i.ToString() + "-" + DateTime.Now.ToString("yyyy年MM月dd日HH点mm分ss") + ".txt", RichTextBoxStreamType.PlainText);
            }

        }
    }
}
