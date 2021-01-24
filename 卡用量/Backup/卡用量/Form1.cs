using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Data.SqlClient;

namespace 卡用量
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }


        private void button1_Click(object sender, EventArgs e)
        {
            SqlConnection conn = new SqlConnection();
            conn.ConnectionString = "Data Source=192.168.2.6;Initial Catalog=unicom;User Id=sa;Password=zitaodellborn2012.,;";
            string date1 = dateTimePicker1.Text;
            string date2 = dateTimePicker2.Text;
            conn.Open();
            string count30 = "SELECT COUNT(*) AS Expr1 FROM Account13800 " +
                              "WHERE (Createtime > '" + date1 + "') AND (Amount = '30') AND (Createtime < '" + date2 + "')";
            string count50 = "SELECT COUNT(*) AS Expr1 FROM Account13800 " +
                              "WHERE (Createtime > '" + date1 + "') AND (Amount = '50') AND (Createtime < '" + date2 + "')";
            string count100 = "SELECT COUNT(*) AS Expr1 FROM Account13800 " +
                              "WHERE (Createtime > '" + date1 + "') AND (Amount = '100') AND (Createtime < '" + date2 + "') and forcity='全国'";
            string countln100 = "SELECT COUNT(*) AS Expr1 FROM Account13800 " +
                              "WHERE (Createtime > '" + date1 + "') AND (Amount = '100') AND (Createtime < '" + date2 + "')and forcity='辽宁'";
            string ucount20 = "SELECT COUNT(*) AS Expr1 FROM AccountUnicom2Netcom " +
                              "WHERE (Createtime > '" + date1 + "') AND (Amount = '20') AND (Createtime < '" + date2 + "')";
            string ucount30 = "SELECT COUNT(*) AS Expr1 FROM AccountUnicom2Netcom " +
                               "WHERE (Createtime > '" + date1 + "') AND (Amount = '30') AND (Createtime < '" + date2 + "')";
            string ucount50 = "SELECT COUNT(*) AS Expr1 FROM AccountUnicom2Netcom " +
                              "WHERE (Createtime > '" + date1 + "') AND (Amount = '50') AND (Createtime < '" + date2 + "')";
            string ucount100 = "SELECT COUNT(*) AS Expr1 FROM AccountUnicom2Netcom " +
                              "WHERE (Createtime > '" + date1 + "') AND (Amount = '100') AND (Createtime < '" + date2 + "')";

            SqlCommand cmd = new SqlCommand(count30, conn);
            label3.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(count50, conn);
            label5.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(count100, conn);
            label7.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(countln100, conn);
            label32.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(ucount20, conn);
            label16.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(ucount30, conn);
            label12.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(ucount50, conn);
            label10.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(ucount100, conn);
            label8.Text = cmd.ExecuteScalar().ToString();



            string kmcount30 = "SELECT COUNT(*) AS Expr1 FROM AccountPswOnline " +
                             "WHERE (Createtime > '" + date1 + "') AND (Classname = '13800卡密') AND (Amount = '30') AND (Createtime < '" + date2 + "')";
            string kmcount50 = "SELECT COUNT(*) AS Expr1 FROM AccountPswOnline " +
                              "WHERE (Createtime > '" + date1 + "') AND (Classname = '13800卡密') AND (Amount = '50') AND (Createtime < '" + date2 + "')";
            string kmcount100 = "SELECT COUNT(*) AS Expr1 FROM AccountPswOnline " +
                              "WHERE (Createtime > '" + date1 + "') AND (Classname = '13800卡密') AND (Amount = '100') AND (Createtime < '" + date2 + "')";

            string kmucount20 = "SELECT COUNT(*) AS Expr1 FROM AccountPswOnline " +
                              "WHERE (Createtime > '" + date1 + "') and  classname='联通卡密' AND (Amount = '20') AND (Createtime < '" + date2 + "')";
            string kmucount30 = "SELECT COUNT(*) AS Expr1 FROM AccountPswOnline " +
                               "WHERE (Createtime > '" + date1 + "') and  classname='联通卡密' AND (Amount = '30') AND (Createtime < '" + date2 + "')";
            string kmucount50 = "SELECT COUNT(*) AS Expr1 FROM AccountPswOnline " +
                              "WHERE (Createtime > '" + date1 + "') and  classname='联通卡密' AND (Amount = '50') AND (Createtime < '" + date2 + "')";
            string kmucount100 = "SELECT COUNT(*) AS Expr1 FROM AccountPswOnline " +
                              "WHERE (Createtime > '" + date1 + "') and  classname='联通卡密' AND (Amount = '100') AND (Createtime < '" + date2 + "')";

            cmd = new SqlCommand(kmcount30, conn);
            label18.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(kmcount50, conn);
            label20.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(kmcount100, conn);
            label22.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(kmucount20, conn);
            label26.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(kmucount30, conn);
            label25.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(kmucount50, conn);
            label23.Text = cmd.ExecuteScalar().ToString();
            cmd = new SqlCommand(kmucount100, conn);
            label30.Text = cmd.ExecuteScalar().ToString();
        
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            dateTimePicker2.Value = dateTimePicker1.Value.AddDays(1);
        }
    }
}
