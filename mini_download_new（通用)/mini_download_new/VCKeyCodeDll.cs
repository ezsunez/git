using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.InteropServices;
 

public class VCKeyCodeDll
{
    public VCKeyCodeDll()
    {
        idx = InitKeyCode(0, System.Text.Encoding.ASCII.GetBytes(passWord));
    }


    /// <summary>
    /// 设置自己的密码进行初始化识别库
    /// </summary>
    /// <param name="pass"></param>
    public VCKeyCodeDll(String pass)
    {
        passWord = pass;
        idx = InitKeyCode(0, System.Text.Encoding.ASCII.GetBytes(passWord));
    }

    /// <summary>
    /// 保存当前初始化标记，对每个线程，此值应该是不同的
    /// </summary>
    private int idx = 0;
    ~VCKeyCodeDll()
    {
        FreeKeyCode();
    }

    /// <summary>
    /// 默认密码
    /// </summary>
    private string passWord = "82315498--BwbYz1CeSdOSJTj`lRSP)>P$=@cCto*r-=J*3?4W>Lt%r>(khad?^J>p$l]/I}GA";


    /// <summary>
    /// 初始化识别库，返回负数表示失败，返回idx用于后面所有函数中的idx
    /// </summary>
    /// <param name="type">库类型，默认为0，只有多个库时此值才起作用</param>
    /// <param name="pass">密码字节值，要以gb2312编码传进来</param>
    /// <returns></returns>
    [DllImport("KeyCodeDll.dll", EntryPoint = "IInitKeyCode")]
    public static extern int InitKeyCode(int type,byte[] pass);

    /// <summary>
    ///释放识别库,其它idx是InitKeyCode函数的返回值
    /// </summary>
    /// <param name="idx">此值为调用InitKeyCode返回的唯一标记值</param>
    /// <returns></returns>
    [DllImport("KeyCodeDll.dll", EntryPoint = "IFreeKeyCode")]
    public static extern int FreeKeyCode(int idx);

     


    ///<summary>
    /// 从内存流进行识别
    ///</summary>
    /// <param name="bs">从网络流上或是从文件读取到的字节值，如果是使用HTTP，则要去掉HTTP头</param>
    /// <param name="len">字节值的长度</param>
    /// <param name="outBuffer">识别结果返回值，建议使用StringBuilder outbuf = new StringBuilder(1000);进行声明</param>
    /// <param name="idx">此值为调用InitKeyCode返回的唯一标记值</param>
    /// <returns>
    /// 返回图片中字符个数，如果小于等于0表示失败，为0表示图片识别结果不正常，负值表示初始化库失败或是图片不正确
    /// </returns>
    [DllImport("KeyCodeDll.dll", EntryPoint = "IGetCodeFromStreamBuffer")]
    public static extern int GetCodeFromStreamBuffer(byte[] bs,int len, StringBuilder outBuffer, int idx);

 
  
    /// <summary>
    /// 
    /// </summary>
    /// <returns></returns>
    public int GetCodeMaxValue()
    {
        return 0;
    }



    public string GetCodeFromStream(byte[] bs, int nLen)
    {
        if (idx < 0)
        {//还没有初始化
            idx = InitKeyCode(0, System.Text.Encoding.ASCII.GetBytes(passWord));
            if (idx < 0)
            {//初始化失败
                System.Windows.Forms.MessageBox.Show("未初始化或初始化失败");
                return "";
            }
        }
        StringBuilder outbuf = new StringBuilder(500);
        int nRet = GetCodeFromStreamBuffer(bs, nLen, outbuf, idx);
        if (nRet <= 0)
        {
            return "";
        }
        return outbuf.ToString();
    }

    /// <summary>
    /// 一般用于外部直接调用
    /// </summary>
    /// <param name="filename">本地文件名</param>
    /// <returns>返回字符串，如果为空里没空或是null则表示失败</returns>
    public string GetCode(string filename)
    {
        if (idx < 0)
        {//还没有初始化
            idx = InitKeyCode(0, System.Text.Encoding.ASCII.GetBytes(passWord));
            if (idx < 0)
            {//初始化失败
                System.Windows.Forms.MessageBox.Show("未初始化或初始化失败");
                return "";
            }
        }
        byte[] bs = System.IO.File.ReadAllBytes(filename);
        string ret = GetCodeFromStream(bs, bs.Length); 
        return ret;
    }


    /// <summary>
    /// 释放
    /// </summary>
    /// <returns></returns>
    private int FreeKeyCode()
    {
        FreeKeyCode(idx);
        idx = -1;
        return 0;
    }

}




 