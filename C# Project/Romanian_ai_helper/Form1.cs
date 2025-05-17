using System.Diagnostics;
using System.Text;

namespace Romanian_ai_helper
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            String inputText = richTextBox1.Text;
            string result;
            switch (comboBox1.SelectedIndex)
            {
                case 0: //Adauga diacritice
                    result = RunPythonScript(inputText);
                    
                    break;
                default:
                    result = RunPythonScript(inputText);
                    break;
            }

            richTextBox1.Text = result;
        }

        string pythonExe = "python";
        string scriptPath = @"C:\Users\adibo_s4utxbj\Documents\PersonalProjects\Romanian_ai_helper\Python script\python_script.py";

        private string RunPythonScript(string inputText)
        {
            var psi = new ProcessStartInfo
            {
                FileName = pythonExe,
                Arguments = $"\"{scriptPath}\" \"{inputText}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8
            };
            try
            {
                using (var process = Process.Start(psi))
                {
                    string output = process.StandardOutput.ReadToEnd();
                    string error = process.StandardError.ReadToEnd();

                    if (!string.IsNullOrEmpty(error))
                        return $"[Error]\n{error}";
                    return output.Trim();
                }
            }
            catch(Exception ex)
            {
                return $"[Exception]\n{ex.Message}";
            }

        }
    }
}
