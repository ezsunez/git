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
            string pattern = @"[0-9]{19}";
            Regex regex = new Regex(pattern);
            var arr = regex.Matches(input).Cast<Match>().ToArray();
            string amount = "";
            if (comboBox1.Text == "100.00") amount = "10.00";
            else amount = comboBox1.Text;
            string sn1 = amount.Substring(0, amount.IndexOf(".00")) + DateTime.Now.Year.ToString().Substring(2, 2) + DateTime.Now.ToString("MMddHHmm");
            richTextBox1.Clear();
            int sn2 = 0;
            string sn = "";
            foreach (var i in arr)
            {
                sn2++;
                 if (sn2 > 99)
                { sn = sn1 + sn2.ToString(); }
                else if(sn2 < 10)
                { sn=sn1 + "00" + sn2.ToString(); }
                else if (sn2>9)
                    { sn = sn1 +"0"+ sn2.ToString(); }
                
                richTextBox1.Text += sn + "\t" + i.Value.Trim() + "\t"+ comboBox1.Text + Environment.NewLine;
                     }
            string dk = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
            richTextBox1.SaveFile(dk + "\\130"+comboBox1.Text.Substring(0, comboBox1.Text.IndexOf(".00"))+"mini-"+sn2.ToString()+"-"+ DateTime.Now.ToString("yyyy年MM月dd日HH点mm分ss")+".txt", RichTextBoxStreamType.PlainText);
        }
    }
}
