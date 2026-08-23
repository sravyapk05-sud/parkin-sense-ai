
import 'login.dart';
import 'profile%20main.dart';
import 'sendcomplaint.dart';
import 'viewdoctors.dart';
// import 'viewtestdetails.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'Viewbookingdetails.dart';
import 'changepassword.dart';

void main() => runApp(MyApp());

class MyApp extends StatefulWidget {
  static const header = 'GeeksforGeeks';

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: header,
      home: MyHomePage(title: header),
    );
  }

  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    throw UnimplementedError();
  }
}




class Services {
  var name;
  var photo;
  get_user() async {
    SharedPreferences pref = await SharedPreferences.getInstance();


    name = pref.getString('name');
    photo = pref.getString('photo');
    return {'name': name, 'photo': photo};
  }
}
class MyHomePage extends StatelessWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;




  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
        backgroundColor: Colors.black12,
      ),
      body: const Center(
        child: Text(
          'Parkinsons',
          style: TextStyle(fontSize: 20),
        ),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.black12,
              ),
              child:
              Column(children: [

                Text(
                  'CT Scan',
                  style: TextStyle(fontSize: 25),

                ),
                CircleAvatar(radius: 30,),
                Text("Name"),
                Text("Email"),

              ])


              ,
            ),
            ListTile(
              leading: Icon(Icons.home),
              title: const Text('Home'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => MyHomePage(title: "Home",),));
              },
            ),
            ListTile(
              leading: Icon(Icons.person_pin),
              title: const Text(' View Profile '),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => MyAppProfilr(),));
              },
            ),
            ListTile(
              leading: Icon(Icons.person_pin_outlined),
              title: const Text(' View Experts '),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => ViewDoctors(title: "Experts",),));
              },
            ),
            ListTile(
              leading: Icon(Icons.book_outlined),
              title: const Text(' View Booking Details '),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => ViewBookingDetailsPage(title: "Booking Details",),));
              },
            ),
            // ListTile(
            //   leading: Icon(Icons.medical_services_outlined),
            //   title: const Text(' View Test Details '),
            //   onTap: () {
            //     Navigator.pop(context);
            //     Navigator.push(context, MaterialPageRoute(builder: (context) => ViewTestDetailsPage(title: "Test Details",),));
            //   },
            // ),

            // ListTile(
            //   leading: Icon(Icons.feed_outlined),
            //   title: const Text('Complaint '),
            //   onTap: () {
            //     Navigator.pop(context);
            //     Navigator.push(context, MaterialPageRoute(builder: (context) => SendComplaintPage(),));
            //   },
            // ),

            ListTile(
              leading: Icon(Icons.change_circle),
              title: const Text(' Change Password '),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(builder: (context) => MyChangePasswordPage(title: "Change Password",),));
              },
            ),
            ListTile(
              leading: Icon(Icons.logout),
              title: const Text('LogOut'),
              onTap: () {

                Navigator.push(context, MaterialPageRoute(builder: (context) => MyLogin(),));
              },
            ),
          ],
        ),
      ),
    );
  }

  s() {

    return Text('');


  }
}