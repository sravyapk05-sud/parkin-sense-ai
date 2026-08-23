import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'login.dart';

void main() {
  runApp(const HospitalSignupApp());
}

class HospitalSignupApp extends StatelessWidget {
  const HospitalSignupApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'User Signup',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueAccent),
        useMaterial3: true,
      ),
      home: const HospitalSignupPage(title: 'User Registration'),
    );
  }
}

class HospitalSignupPage extends StatefulWidget {
  const HospitalSignupPage({super.key, required this.title});
  final String title;

  @override
  State<HospitalSignupPage> createState() => _HospitalSignupPageState();
}

class _HospitalSignupPageState extends State<HospitalSignupPage> {
  final _formKey = GlobalKey<FormState>();

  TextEditingController nameController = TextEditingController();
  TextEditingController emailController = TextEditingController();
  TextEditingController phoneController = TextEditingController();
  TextEditingController passwordController = TextEditingController();
  TextEditingController cpController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        backgroundColor: Colors.blueAccent,
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            children: [


              // ------------------- Personal Info -------------------
              const Align(
                alignment: Alignment.centerLeft,
                child: Text("Personal Info", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
              ),
              const SizedBox(height: 10),

              TextFormField(
                controller: nameController,
                decoration: _inputDecoration('Full Name', Icons.person),
                validator: (v) => v!.isEmpty ? 'Enter full name' : null,
              ),
              const SizedBox(height: 10),



              // ------------------- Contact Info -------------------
              const Align(
                alignment: Alignment.centerLeft,
                child: Text("Contact Info", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
              ),
              const SizedBox(height: 10),

              TextFormField(
                controller: emailController,
                keyboardType: TextInputType.emailAddress,
                decoration: _inputDecoration('Email', Icons.email_outlined),
                validator: (v){
                  if(v!.isEmpty || !RegExp(r"^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}").hasMatch(v)) {
                    return 'Enter valid email';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 10),

              TextFormField(
                controller: phoneController,
                keyboardType: TextInputType.phone,
                decoration: _inputDecoration('Phone', Icons.phone),
                validator: (v)=> v!.isEmpty ? 'Enter phone number' : null,
              ),

              const SizedBox(height: 20),


              // ------------------- Account -------------------
              const Align(
                alignment: Alignment.centerLeft,
                child: Text("Account", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
              ),
              const SizedBox(height: 10),

              TextFormField(
                controller: passwordController,
                obscureText: true,
                decoration: _inputDecoration('Password', Icons.lock),
                validator: (v)=> v!.isEmpty ? 'Enter password' : null,
              ),
              const SizedBox(height: 10),

              TextFormField(
                controller: cpController,
                obscureText: true,
                decoration: _inputDecoration('Confirm Password', Icons.lock),
                validator: (v){
                  if(v!.isEmpty) return 'Enter confirm password';
                  if(v!=passwordController.text) return 'Passwords do not match';
                  return null;
                },
              ),

              const SizedBox(height: 30),

              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _submitForm,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueAccent,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
                  ),
                  child: const Text("Register", style: TextStyle(fontSize: 18)),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }

  InputDecoration _inputDecoration(String label, IconData icon) {
    return InputDecoration(
      labelText: label,
      prefixIcon: Icon(icon, color: Colors.teal),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(25)),
      floatingLabelBehavior: FloatingLabelBehavior.auto,
    );
  }

  void _submitForm() async {
    if (!_formKey.currentState!.validate()) {
      Fluttertoast.showToast(msg: "Please fill all fields");
      return;
    }
    _sendData();
  }

  Future<void> _sendData() async {
    SharedPreferences sh = await SharedPreferences.getInstance();
    String url = sh.getString('url') ?? '';

    final response = await http.post(Uri.parse('$url/myapp/and_signup/'), body: {
      'name': nameController.text,
      'email': emailController.text,
      'phonenumber': phoneController.text,
      'password': passwordController.text,
      'confirmpassword': cpController.text,
    });

    if (response.statusCode == 200) {
      String status = jsonDecode(response.body)['status'];
      if (status == 'ok') {
        Fluttertoast.showToast(msg: 'Registration Successful');
        Navigator.push(context, MaterialPageRoute(builder: (context) => MyLogin()));
      } else {
        Fluttertoast.showToast(msg: 'Registration Failed');
      }
    } else {
      Fluttertoast.showToast(msg: 'Network Error');
    }
  }
}
