using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Diagnostics;
using System.Threading;
using System.Runtime.InteropServices;
using System.Data.OleDb;
using Microsoft.Win32;
using System.IO;


namespace mini_download_new
{
    public partial class Form1 : Form
    {
        private System.Threading.Timer ti;
        private System.Threading.Timer ti1;
        private System.Threading.Timer ti2;
        public Form1()
        {
            InitializeComponent();
            ti = new System.Threading.Timer(new TimerCallback(t), null, 0, 1000);
            
          
        }
        int iiii = 1;
        void tim()
        {
            ti = new System.Threading.Timer(new TimerCallback(t), null, 0, 1000);
        }

        OleDbConnection conn = new OleDbConnection(@"Provider=Microsoft.Jet.OLEDB.4.0;Data Source="+Application.StartupPath +"\\mac.mdb;"  );

        string zcb = "0001";
        string minilj = @"C:\Program Files\China Unicom\PC MINI\CUMini";
        string zmlj = @"C:\Documents and Settings\Administrator\桌面";
        string wllj = "本地连接";
        string wlqy = "启用";
        string wlty = "停用";
        string file = @"C:\Documents and Settings\Administrator\桌面\miniTEMP.txt";
        string fileyuan = @"C:\Documents and Settings\Administrator\桌面\miniTEMP原文件.txt";


        public int GetRows(string FilePath)
        {
            using (StreamReader read = new StreamReader(FilePath, Encoding.Default))
            {
                return read.ReadToEnd().Split('\n').Length;
                read.Dispose();
            }
        }

        public void CloseSoundApp()
        {
            MessageBox.Show("下完了");
            Process[] pProcess;
            pProcess = Process.GetProcesses();
            for (int i = 1; i <= pProcess.Length - 1; i++)
            {
                if (pProcess[i].ProcessName == "CUMini")
                {
                    pProcess[i].Kill();
                    break;
                }
            }
       
        }


        private void InvokeControl()
        {
         
          this.Invoke(new DelegateChangeText(ChangeText));
           
        }

        private void ChangeText()
        {
            
            label3.Text = (GetRows(file) - 1).ToString() + "张";
            label2.Text = times.ToString();
        }

        public delegate void DelegateChangeText();
        public delegate void a();

        private void InvokeControl1()
        {

            this.Invoke(new a(bbb));

        }

        private void bbb()
        {
            checkBox1.Checked = true;
        }

        private void t1(object a)
        {
            ti1.Dispose();


            IntPtr hwndCalc = FindWindow(null, "提示");
            if (hwndCalc != IntPtr.Zero)
            {
                IntPtr hwndmm = FindWindowEx(hwndCalc, IntPtr.Zero, "Edit", null);

                if (hwndmm != IntPtr.Zero)
                {
                    StringBuilder textmm = new StringBuilder(600);
                    SendMessage_Ex(hwndmm, WM_GETTEXT, 600, textmm);
                    if (textmm.ToString().IndexOf("验证码错误") != -1)
                    {
                        IntPtr hwndThree = FindWindowEx(hwndCalc, IntPtr.Zero, "Button", "确定");
                        SendMessage(hwndThree, BM_CLICK, 0, null);
                        IntPtr hwnd1 = FindWindow(null, "中国联通Mini终端─业务密码");
                        if (hwnd1 != IntPtr.Zero)
                        {
                            IntPtr hwnde = FindWindowEx(hwnd1, IntPtr.Zero, "Button", "换一张");
                            SendMessage(hwnde, BM_CLICK, 0, null);
                            Thread.Sleep(500);
                            yzm();
                            hwndThree = FindWindowEx(hwnd1, IntPtr.Zero, "Button", "确定");
                            SendMessage(hwndThree, BM_CLICK, 0, null);
                        }
                    }
                }
            }           
        }


        private void t2(object a)
        {
            ti2.Change(Timeout.Infinite, Timeout.Infinite);
            
            IntPtr hwnd1a = FindWindow(null, "询问");
            if (hwnd1a != IntPtr.Zero)
            {
                IntPtr hwnd2 = FindWindowEx(hwnd1a, IntPtr.Zero, "Edit", null);
                StringBuilder textmm = new StringBuilder(600);
                SendMessage_Ex(hwnd2, WM_GETTEXT, 600, textmm);
                if (textmm.ToString().IndexOf("确定要退出MINI终端系统吗？") != -1)
                {
                    IntPtr hwndThree = FindWindowEx(hwnd1a, IntPtr.Zero, "Button", "确定");
                    if (hwndThree != IntPtr.Zero)
                    {
                        SendMessage(hwndThree, BM_CLICK, 0, null);
                        CloseSoundApp();
                    }
                }
            }
            else { ti2.Change(0, 1000); }
            
        }

        private void t(object a)
        {
            //ti.Dispose();

            ti.Change(Timeout.Infinite, Timeout.Infinite);
            IntPtr hwnd1 = FindWindow(null, "询问");
            if (hwnd1 != IntPtr.Zero)
            {
                IntPtr hwnd2 = FindWindowEx(hwnd1, IntPtr.Zero, "Edit", null);
                StringBuilder textmm = new StringBuilder(600);
                SendMessage_Ex(hwnd2, WM_GETTEXT, 600, textmm);
                if (textmm.ToString().IndexOf("确定要提交本次交易") != -1)
                {
                    hwnd2 = FindWindowEx(hwnd1, IntPtr.Zero, "Button", "确定");
                    SendMessage(hwnd2, BM_CLICK, 0, null);
                }

            }

            hwnd1 = FindWindow(null, "中国联通Mini终端─业务密码");
            if (hwnd1 != IntPtr.Zero)
            {
                IntPtr hwnd2 = FindWindowEx(hwnd1, IntPtr.Zero, "Edit", null);
                SendMessage(hwnd2, WM_SETTEXT, 0, "700512");
                yzm();
                ti1 = new System.Threading.Timer(new TimerCallback(t1), null, 500, 1000);
                IntPtr hwndThree = FindWindowEx(hwnd1, IntPtr.Zero, "Button", "确定");
                SendMessage(hwndThree, BM_CLICK, 0, null); 
            }

            IntPtr hwndCalc = FindWindow(null, "提示");
            if (hwndCalc != IntPtr.Zero)
            {
                IntPtr hwndmm = FindWindowEx(hwndCalc, IntPtr.Zero, "Edit", null);

                if (hwndmm != IntPtr.Zero)
                {
                    StringBuilder textmm = new StringBuilder(600);
                    SendMessage_Ex(hwndmm, WM_GETTEXT, 600, textmm);
                    string aa = "电子卡购买成功！";
                   string bb = "卡号：";
                   string cc = "aaaaa";
                   if (textmm.ToString().IndexOf(aa) != -1)
                   { cc = aa; }
                   else if (textmm.ToString().IndexOf(bb) != -1)
                   {
                       
                       if (MessageBox.Show("是否将此卡密添加到文件？", "", MessageBoxButtons.YesNo) == DialogResult.Yes)
                       {
                           cc = bb;
                           textmm.Replace("元", ".00");
                       }
                       else
                       {
                           IntPtr hwndxw = FindWindow(null, "提示");
                           IntPtr hwnd2 = FindWindowEx(hwndxw, IntPtr.Zero, "Button", "确定");
                           SendMessage(hwnd2, BM_CLICK, 0, null);
                       }
                       
                   }
                       if (textmm.ToString().IndexOf(cc) != -1)
                       {
                           cc = "aaaaa";
                           string outmm = "";
                           int num = 0;
                           string amount = textmm.ToString().Substring(textmm.ToString().IndexOf("面值：") + 3, (textmm.ToString().IndexOf(".00") - (textmm.ToString().IndexOf("面值：") )));
                           int begin = textmm.ToString().IndexOf("卡号：", num);

                           while (begin != -1)
                           {


                               string mm = textmm.ToString().Substring(begin + 3, 15) + "\t" + textmm.ToString().Substring(begin + 19 + 5, 19) + "\t" + amount + "\n";
                               outmm += mm;
                               num = begin + 3;
                               begin = textmm.ToString().IndexOf("卡号：", num);
                           }
                           System.IO.StreamWriter xA = new System.IO.StreamWriter(file, true, System.Text.Encoding.Default);
                           //true换成False是替换 反之是覆盖 
                           xA.Write(outmm.Replace("\n", System.Environment.NewLine));
                           xA.Close();


                           string yuan = textBox1.Text + "---" + textmm.ToString() + "\n" + "\n";
                           System.IO.StreamWriter xAyuan = new System.IO.StreamWriter(fileyuan, true, System.Text.Encoding.Default);
                           //true换成False是替换 反之是覆盖 
                           xAyuan.Write(yuan.Replace("\n", System.Environment.NewLine) + "\n" + "\n");
                           xAyuan.Close();
                           yuan = "";
                           IntPtr hwndxw = FindWindow(null, "提示");
                           IntPtr hwnd2 = FindWindowEx(hwndxw, IntPtr.Zero, "Button", "确定");
                           SendMessage(hwnd2, BM_CLICK, 0, null);
                           ++times;
                           hwndxw = FindWindow(null, "询问");
                           hwnd2 = FindWindowEx(hwndxw, IntPtr.Zero, "Button", "否");
                           SendMessage(hwnd2, BM_CLICK, 0, null);
                           InvokeControl();
                           hwndCalc = FindWindow(null, "中国联通Mini终端");

                           SetForegroundWindow(hwndCalc);
                           if (times <= timesmax)
                           {
                             
                               InvokeControl1();
                           }
                           else
                           {
                               close();
                           }
                       }
                }

            }
            
            Thread.Sleep(100);
            ti.Change(500, 1000);
        }

        [DllImport("user32.dll", EntryPoint = "FindWindow", SetLastError = true)]         //找程序窗口
        private static extern IntPtr FindWindow(string lpClassName, string lpWindowName);

        [DllImport("user32.dll", EntryPoint = "FindWindowEx", SetLastError = true)]     //找控件
        private static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);

        [DllImport("user32.dll", EntryPoint = "SetForegroundWindow", SetLastError = true)]   //设置到最前窗口
        private static extern void SetForegroundWindow(IntPtr hwnd);

        [DllImport("Project1.dll", EntryPoint = "GetWndPic", SetLastError = true)]       
         private static extern IntPtr GetWndPic(IntPtr hwnd, PictureBox Pic);

       [ DllImport("user32.dll", EntryPoint = "SendMessageA")]
        private static extern int SendMessage_Ex(IntPtr hwnd, int wMsg, int wParam, StringBuilder lParam);

        [DllImport("user32.dll", EntryPoint = "SendMessage", SetLastError = true, CharSet = CharSet.Auto)]   //窗口输入
        private static extern int SendMessage(IntPtr hwnd, uint wMsg, int wParam, string lParam);
        const int WM_SETTEXT = 0x000C;
        const int WM_GETTEXT = 0x000D;
        const int CB_SETCURSEL = 0x14E;
        const uint BM_CLICK = 0xF5;

        
        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog opf = new OpenFileDialog();
            opf.Filter = "文本文件(*.txt)|*.txt";
            opf.ShowDialog();
            string file1 = opf.FileName;
            if (file1 != "")
            {
                label3.Text = (GetRows(file1) - 1).ToString() + "张";
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
           
            timer1.Enabled = false;
            IntPtr hwnd1 = FindWindow(null, "中国联通Mini终端");                // 登陆密码
            SetForegroundWindow(hwnd1);
            if (hwnd1 != IntPtr.Zero)
            {
                Thread.Sleep(500);
                IntPtr hwnd2 = FindWindowEx(hwnd1, IntPtr.Zero, "Edit", null);
                SendMessage(hwnd2, WM_SETTEXT, 0, "888888");
                IntPtr hwnd3 = FindWindowEx(hwnd1, IntPtr.Zero, "Button", "确定");
                SendMessage(hwnd3, BM_CLICK, 0, null);
                timer2.Enabled = true;
            }
            else { timer1.Enabled = true; }
        }

        private void timer2_Tick(object sender, EventArgs e)
        {
            timer2.Enabled = false;
            IntPtr hwnd1 = FindWindow(null, "中国联通Mini终端");
            if (hwnd1 != IntPtr.Zero)
            {
                IntPtr hwnd2 = FindWindowEx(hwnd1, IntPtr.Zero, null , "购买电子卡");
                if (hwnd2 != IntPtr.Zero)
                {
                    SendMessage(hwnd2, BM_CLICK, 0, null);
                    chosse_amount();
                   
                    
                }
                else { timer2.Enabled = true; }
            }
            else { timer2.Enabled = true; }
        }
        int times = 1;
        int timesmax = 0;

        void chosse_amount()
        {
            int amount = -1;
            int count = 5;
            if (radioButton1.Checked == true)
            {
                amount = 0;
                timesmax = 10;
            }
            if (radioButton2.Checked == true)
            {
                amount = 1;
                if (times == 1)
                {
                    count = 3;
                }
                timesmax = 7;
            }
            if (radioButton3.Checked == true)
            {
                amount = 2;
                timesmax = 4;
            }
            if (radioButton4.Checked == true)
            {
                amount = 3;
                timesmax = 2;
            }
            IntPtr hwnd1 = FindWindow(null, "中国联通Mini终端");
            IntPtr hwndThree = FindWindowEx(hwnd1, IntPtr.Zero, "#32770", null );
            hwndThree = FindWindowEx(hwnd1, hwndThree, "#32770", null);
            hwndThree = FindWindowEx(hwnd1, hwndThree, "#32770", null);
            hwndThree = FindWindowEx(hwnd1, hwndThree, "#32770", null);
            hwndThree = FindWindowEx(hwndThree, IntPtr.Zero , "#32770", "中国联通Mini终端");
            IntPtr hwndcomb = FindWindowEx(hwndThree, IntPtr.Zero, "ComboBox", null);
            SendMessage(hwndcomb, CB_SETCURSEL, amount, null);
            IntPtr hwndcou = FindWindowEx(hwndThree, IntPtr.Zero, "Edit", null);
            SendMessage(hwndcou, WM_SETTEXT, 0, count.ToString());

            IntPtr hwndsubmit = FindWindowEx(hwndThree, IntPtr.Zero, "Button", "确定");
            SendMessage(hwndsubmit, BM_CLICK, 0, null);

        }

    
   

     
        private void  Form1_Load(object sender, EventArgs e)
        {
            System.Diagnostics.Process[] myProcesses = System.Diagnostics.Process.GetProcessesByName("mini_download_new");//获取指定的进程名   
            if (myProcesses.Length > 1) //如果可以获取到知道的进程名则说明已经启动
            {
                MessageBox.Show("程序已启动！");
                Application.Exit();              //关闭系统
            }

        }

        private void button3_Click(object sender, EventArgs e)
        {
            macchange(1);


        }

        private string[]    macchange(int i)
        {
            if (i == 1)
            {
                string sql = "select * from mac_list where id=" + textBox1.Text;
                OleDbCommand myCommand = new OleDbCommand(sql, conn);
                conn.Open();
                OleDbDataReader reader = myCommand.ExecuteReader(); ;
                string mac = null;
                if (reader.Read())
                {
                    mac = reader[1].ToString();
                }
                conn.Close();
                RegistryKey key = Registry.LocalMachine;

                RegistryKey software = key.OpenSubKey("SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\" + zcb, true); //该项必须已存在
                software.SetValue("NetworkAddress", mac);
                NetWork(wllj, wlty);
                Thread.Sleep(1000);
                NetWork(wllj, wlqy);
                Process.Start(minilj, "");
                
                times = 1;
                label2.Text = "0";
            }
            timer1.Enabled = true;
                string kind = "";
            
            if (radioButton1.Checked == true)
            {
                kind = radioButton1.Text;
            }
            if (radioButton2.Checked == true)
            {
                kind = radioButton2.Text;
            }
            if (radioButton3.Checked == true)
            {
                kind = radioButton3.Text;
            }
            if (radioButton4.Checked == true)
            {
                kind = radioButton4.Text;
            }
            string time = DateTime.Now.ToString("MM月dd日HH点mm分ss秒");
            string [] at =new string []{kind ,time };
            return at;
        }
        public void NetWork(string netWorkName, string operation1)
        {
            int conf = 0;
            do {
            Shell32.Shell shell = new Shell32.ShellClass();
            Shell32.Folder folder = shell.NameSpace(49);
            //指向一个“网络连接”虚拟文件夹对象，49这个数字代表“网络连接”
            foreach (Shell32.FolderItem fi in folder.Items())//遍历“网络连接”这个虚拟文件夹找到跟netWorkName相同的条目
            {
                if (fi.Name != netWorkName)
                    continue;
                Shell32.ShellFolderItem folderItem = (Shell32.ShellFolderItem)fi;
                foreach (Shell32.FolderItemVerb fiv in folderItem.Verbs())//遍历右键菜单找到跟operation相同的条目
                {
                    if (!fiv.Name.Contains(operation1))
                        continue;
                    //else if (!fiv.Name.Contains(operation2))
                    //    continue;
                    else
                    {
                        conf = 1;
                        fiv.DoIt();
                        Thread.Sleep(1000);
                        break;
                    }
                } 
                }
            } while (conf == 0);

        }

        private void close()
        {
            ti2 = new System.Threading.Timer(new TimerCallback(t2), null, 0, 1000);
            IntPtr hwndCalc = FindWindow(null, "中国联通Mini终端");
            IntPtr hwndThree = FindWindowEx(hwndCalc, IntPtr.Zero, null, "自服务");
            SendMessage(hwndThree, BM_CLICK, 0, null);
            IntPtr d1 = FindWindowEx(hwndCalc, IntPtr.Zero, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
             d1 = FindWindowEx(hwndCalc, d1, "Button", "");
            SendMessage(d1, BM_CLICK, 0, null);
            if (d1 == IntPtr.Zero)
            {
                CloseSoundApp();
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            string [] at= macchange(1);
            string kind = at[0];
            string time = at[1];

            file = zmlj + @"\130" + kind + " mini" + time + ".txt";
            FileStream myFs = new FileStream(file, FileMode.Create);
            myFs.Close();
            fileyuan = zmlj + @"\130" + kind + " mini" + time + "原文件.txt";
            FileStream myFs1 = new FileStream(fileyuan, FileMode.Create);
            myFs1.Close();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            close();
            
          
        }

        private void button5_Click(object sender, EventArgs e)
        {
            macchange(0);
        }

        private void button6_Click(object sender, EventArgs e)
        {
            OpenFileDialog opf = new OpenFileDialog();
            opf.Filter = "文本文件(*.txt)|*.txt";
            opf.ShowDialog();
            string all = "";
            using (StreamReader st = new StreamReader(opf.FileName, System.Text.Encoding.GetEncoding("gb2312")))
            {
                all = st.ReadToEnd();
                List<int> num = new List<int>();
                string list = "";
                for (int start = 0; start < all.Length; )
                {
                    int i = all.IndexOf("---", start);
                    if (i != -1)
                    {
                        int n = all.LastIndexOf("\n", i);
                        if (list.IndexOf(all.Substring(n + 1, i - n - 1)) == -1)
                        {
                            list += all.Substring(n + 1, i - n - 1) + ";";
                            num.Add(int.Parse(all.Substring(n + 1, i - n - 1)));
                        }

                        start = ++i;
                    }
                    else { break; }

                }
                string xulie2 = null;
                string xulie0 = num[0].ToString();
                string xulie1 = null;

                for (int no = 1; no < num.Count; no++)
                {
                    if (num[no] == num[no - 1] + 1)
                    {
                        xulie1 = num[no].ToString();
                    }
                    else
                    {
                        xulie2 = num[no].ToString();
                        if (xulie1 != null)
                        {
                            xulie0 += '-' + xulie1 + ";" + xulie2;
                        }
                        else
                        {
                            xulie0 += ";" + xulie2;
                        }
                        xulie1 = null;
                        xulie2 = null;
                    }
                }
                if (xulie1 != null)
                {
                    xulie0 += '-' + xulie1 + ";" + xulie2;
                }

                string qianzhui1 = opf.FileName.Substring(opf.FileName.LastIndexOf(@"\") + 1, opf.FileName.LastIndexOf("m") - opf.FileName.LastIndexOf(@"\") - 2);
                string zhangshulj = opf.FileName.Substring(0, opf.FileName.LastIndexOf("原文件")) + ".txt";
                string zhangshu = (GetRows(zhangshulj) - 1).ToString();
                string quan = qianzhui1 + "-" + zhangshu + "- -" + DateTime.Today.ToString("M.dd") + "-(" + xulie0 + ")";
                Clipboard.SetDataObject(quan);
                textBox1.Text = quan;
                opf.Dispose();
            }
        }

        private void button10_Click(object sender, EventArgs e)
        {
            textBox1.Text = (int.Parse(textBox1.Text) - 1).ToString();
        }

        private void button11_Click(object sender, EventArgs e)
        {
            textBox1.Text = (int.Parse(textBox1.Text) + 1).ToString();
        }


        private void yzm()
        {


            IntPtr hwnd1 = FindWindow(null, "中国联通Mini终端─业务密码");
            if (hwnd1 != IntPtr.Zero)
            {
                IntPtr hwnd2 = IntPtr.Zero;
                int i = 1;
                do
                {

                    hwnd2 = FindWindowEx(hwnd1, hwnd2, "Static", null);
                    //MessageBox.Show(hwnd2.ToString());
                    ++i;
                }
                while (i != 4);

                getp(hwnd2);
            }
        }
        public struct RECT
        {
            public int Left; //最左坐标
            public int Top; //最上坐
            public int Right;
            public int Bottom;

        }
        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        static extern bool GetWindowRect(IntPtr hWnd, out  RECT lpRect);
        [DllImport("user32.dll")]
        public static extern IntPtr GetWindowDC(IntPtr ptr);
        [DllImport("gdi32.dll")]
        public static extern bool BitBlt(IntPtr hdcDest, int nXDest, int nYDest, int wDest, int hDest, IntPtr hdcSource, int xSrc, int ySrc, System.Int32 rop);
        const int SRCCOPY = 0xCC0020;
        VCKeyCodeDll dll = new VCKeyCodeDll();
        public static byte[] Bitmap2Byte(Bitmap bitmap)
        {
            using (MemoryStream stream = new MemoryStream())
            {
                bitmap.Save(stream, System.Drawing.Imaging.ImageFormat.Bmp);
                byte[] data = new byte[stream.Length];
                stream.Seek(0, SeekOrigin.Begin);
                stream.Read(data, 0, Convert.ToInt32(stream.Length));
                return data;
            }
        }
        public void getp(IntPtr hwnd)
        {
            RECT r = new RECT();
            GetWindowRect(hwnd, out  r);  //获得目标窗体的大小
            Bitmap Pic = new Bitmap(r.Right - r.Left, r.Bottom - r.Top);
           
            Graphics g1 = Graphics.FromImage(Pic);
            IntPtr hdc1 = GetWindowDC(hwnd);
            IntPtr hdc2 = g1.GetHdc();  //得到Bitmap的DC
            BitBlt(hdc2, 0, 0, r.Right - r.Left, r.Bottom - r.Top, hdc1, 0, 0, 13369376);
            g1.ReleaseHdc(hdc2);  //释放掉Bitmap的DC
            g1.Dispose();
            //Image newImage = new Bitmap(r.Right - r.Left, r.Bottom - r.Top);
            //g1 = Graphics.FromImage(newImage);
            //g1.DrawImage(Pic, 0, 0);
            //Pic.Dispose();
            //newImage.Save("yzm.bmp", System.Drawing.Imaging.ImageFormat.Bmp);

            byte[] bs = Bitmap2Byte(Pic);
            
                //System.IO.File.ReadAllBytes(Application.StartupPath+@"\yzm.bmp");
            //StringBuilder sb = new StringBuilder();
            string dqdyzm = dll.GetCodeFromStream(bs, bs.Length);
           
            IntPtr hwnd1 = FindWindow(null, "中国联通Mini终端─业务密码");
            if (hwnd1 != IntPtr.Zero)
            {
                IntPtr hwnd2 = IntPtr.Zero;
                int i = 1;
                do
                {

                    hwnd2 = FindWindowEx(hwnd1, hwnd2, "Edit", null);
                    //MessageBox.Show(hwnd2.ToString());
                    ++i;
                }
                while (i != 3);
                SendMessage(hwnd2, WM_SETTEXT, 0, dqdyzm);
            }
            bs = null;
         
            dqdyzm = null;

        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {

            if (checkBox1.Checked == true)
            {
                Random ran = new Random();
                int jg100 = ran.Next(10, 20);
                int jg50 = ran.Next(95, 110);
                int jg = ran.Next(95, 110);
                //MessageBox.Show(jg.ToString());
                if (radioButton4.Checked == true) { Thread.Sleep(jg100 * 1000); }
                else if (radioButton3.Checked == true) { Thread.Sleep(jg50 * 1000); }
                else { Thread.Sleep(jg * 1000); }
                macchange(0);
                checkBox1.Checked = false;
            }
        }


    }
}
