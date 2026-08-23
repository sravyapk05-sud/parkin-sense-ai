import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'chat.dart';
import 'sendfeedback.dart';
import 'viewreply.dart';
import 'homenew.dart';

void main() {
  runApp(const ViewBookingDetails());
}

class ViewBookingDetails extends StatelessWidget {
  const ViewBookingDetails({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'View Booking Details',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blueAccent,
          primary: Colors.blueAccent,
          secondary: Colors.lightBlueAccent,
          background: Color(0xFFF8F9FA),
        ),
        useMaterial3: true,
        fontFamily: 'Poppins',
        appBarTheme: AppBarTheme(
          backgroundColor: Colors.blueAccent,
          foregroundColor: Colors.white,
          elevation: 4,
          centerTitle: true,
        ),
      ),
      home: const ViewBookingDetailsPage(title: 'My Appointments'),
    );
  }
}

class ViewBookingDetailsPage extends StatefulWidget {
  const ViewBookingDetailsPage({super.key, required this.title});

  final String title;

  @override
  State<ViewBookingDetailsPage> createState() => _ViewBookingDetailsPageState();
}

class _ViewBookingDetailsPageState extends State<ViewBookingDetailsPage> {
  _ViewBookingDetailsPageState() {
    viewbookingdetails();
  }

  List<String> id_ = <String>[];
  List<String> dlid_ = <String>[];
  List<String> did_ = <String>[];
  List<String> date_ = <String>[];
  List<String> dname_ = <String>[];
  List<String> dphone_ = <String>[];
  List<String> dsched_ = <String>[];
  bool _isLoading = true;

  Future<void> viewbookingdetails() async {
    List<String> id = <String>[];
    List<String> dlid = <String>[];
    List<String> did = <String>[];
    List<String> date = <String>[];
    List<String> dname = <String>[];
    List<String> dphone = <String>[];
    List<String> dsched = <String>[];

    try {
      SharedPreferences sh = await SharedPreferences.getInstance();
      String urls = sh.getString('url').toString();
      String lid = sh.getString('lid').toString();
      String url = '$urls/myapp/and_user_view_appointment/';

      var data = await http.post(Uri.parse(url), body: {
        "lid": lid,
      });

      var jsondata = json.decode(data.body);
      String statuss = jsondata['status'];

      var arr = jsondata["data"];

      print(arr.length);

      for (int i = 0; i < arr.length; i++) {
        id.add(arr[i]['id'].toString());
        dlid.add(arr[i]['dlid'].toString());
        did.add(arr[i]['did'].toString());
        date.add(arr[i]['date']);
        dname.add(arr[i]['dname']);
        dphone.add(arr[i]['dphone']);
        dsched.add(arr[i]['sched']);
      }

      setState(() {
        id_ = id;
        dlid_ = dlid;
        did_ = did;
        date_ = date;
        dname_ = dname;
        dphone_ = dphone;
        dsched_ = dsched;
        _isLoading = false;
      });

      print(statuss);
    } catch (e) {
      print("Error ------------------- " + e.toString());
      setState(() {
        _isLoading = false;
      });
    }
  }

  Widget _buildInfoRow(String label, String value, IconData icon, Color iconColor) {
    return Container(
      margin: EdgeInsets.symmetric(vertical: 6),
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: Colors.blueAccent.withOpacity(0.1),
          width: 1,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.blueAccent.withOpacity(0.05),
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: iconColor.withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(
              icon,
              size: 18,
              color: iconColor,
            ),
          ),
          SizedBox(width: 12),
          Expanded(
            flex: 2,
            child: Text(
              label,
              style: TextStyle(
                fontWeight: FontWeight.w500,
                color: Colors.grey[700],
                fontSize: 14,
              ),
            ),
          ),
          Expanded(
            flex: 3,
            child: Text(
              value,
              style: TextStyle(
                fontWeight: FontWeight.w600,
                color: Colors.blueAccent,
                fontSize: 14,
              ),
              textAlign: TextAlign.right,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionButton(String text, IconData icon, Color color, VoidCallback onPressed) {
    return Expanded(
      child: Container(
        margin: EdgeInsets.symmetric(horizontal: 4),
        child: ElevatedButton.icon(
          onPressed: onPressed,
          icon: Icon(icon, size: 18),
          label: Text(
            text,
            style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: color,
            foregroundColor: Colors.white,
            padding: EdgeInsets.symmetric(vertical: 12, horizontal: 4),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
            elevation: 2,
            shadowColor: color.withOpacity(0.3),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => HomeNewPage(title: "Home"),
          ),
        );
        return false;
      },
      child: Scaffold(
        backgroundColor: Colors.grey[50],
        appBar: AppBar(
          leading: IconButton(
            icon: Icon(Icons.arrow_back, color: Colors.white),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => HomeNewPage(title: "Home")),
              );
            },
          ),
          backgroundColor: Colors.blueAccent,
          title: Text(
            widget.title,
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w600,
              fontSize: 20,
            ),
          ),
          centerTitle: true,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.only(
              bottomLeft: Radius.circular(20),
              bottomRight: Radius.circular(20),
            ),
          ),
        ),
        body: _isLoading
            ? Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(
                valueColor: AlwaysStoppedAnimation<Color>(Colors.blueAccent),
              ),
              SizedBox(height: 16),
              Text(
                'Loading Appointments...',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.blueAccent,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        )
            : id_.isEmpty
            ? Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.calendar_month_outlined,
                size: 80,
                color: Colors.blueAccent.withOpacity(0.4),
              ),
              SizedBox(height: 16),
              Text(
                'No Appointments Found',
                style: TextStyle(
                  fontSize: 20,
                  color: Colors.blueAccent,
                  fontWeight: FontWeight.w600,
                ),
              ),
              SizedBox(height: 8),
              Text(
                'You don\'t have any appointments yet',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey[600],
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        )
            : RefreshIndicator(
          onRefresh: viewbookingdetails,
          backgroundColor: Colors.white,
          color: Colors.blueAccent,
          child: ListView.builder(
            physics: AlwaysScrollableScrollPhysics(),
            padding: EdgeInsets.all(16),
            itemCount: id_.length,
            itemBuilder: (BuildContext context, int index) {
              return Container(
                margin: EdgeInsets.only(bottom: 20),
                child: Card(
                  elevation: 4,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                  shadowColor: Colors.blueAccent.withOpacity(0.1),
                  child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [
                          Colors.white,
                          Colors.blueAccent.withOpacity(0.03),
                        ],
                      ),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Header with Doctor Name
                          Row(
                            children: [
                              Container(
                                padding: EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: Colors.blueAccent.withOpacity(0.1),
                                  shape: BoxShape.circle,
                                ),
                                child: Icon(
                                  Icons.medical_services,
                                  color: Colors.blueAccent,
                                  size: 24,
                                ),
                              ),
                              SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'Dr. ${dname_[index]}',
                                      style: TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.blueAccent,
                                      ),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    SizedBox(height: 4),
                                    Text(
                                      'Medical Specialist',
                                      style: TextStyle(
                                        fontSize: 12,
                                        color: Colors.grey[600],
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              Container(
                                padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                decoration: BoxDecoration(
                                  color: Colors.blueAccent.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  'Confirmed',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.blueAccent,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ),
                            ],
                          ),
                          SizedBox(height: 20),

                          // Appointment Details
                          Text(
                            'Appointment Details',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w600,
                              color: Colors.blueAccent,
                            ),
                          ),
                          SizedBox(height: 12),

                           _buildInfoRow('Appointment Date', dsched_[index], Icons.event, Colors.green),

                          SizedBox(height: 20),

                          // Action Buttons Section
                          Container(
                            padding: EdgeInsets.only(top: 16),
                            decoration: BoxDecoration(
                              border: Border(
                                top: BorderSide(
                                  color: Colors.blueAccent.withOpacity(0.1),
                                  width: 1,
                                ),
                              ),
                            ),
                            child: Row(
                              children: [
                                _buildActionButton(
                                  'Chat',
                                  Icons.chat_outlined,
                                  Colors.blueAccent,
                                      () async {
                                    SharedPreferences sh = await SharedPreferences.getInstance();
                                    sh.setString('dlid', dlid_[index]);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(builder: (context) => MyChatPage(title: 'Chat')),
                                    );
                                  },
                                ),
                                _buildActionButton(
                                  'Feedback',
                                  Icons.reviews_outlined,
                                  Colors.lightBlueAccent,
                                      () async {
                                    SharedPreferences sh = await SharedPreferences.getInstance();
                                    sh.setString('doid', did_[index]);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(builder: (context) => MySendFeedbackPage(title: 'Send Feedback')),
                                    );
                                  },
                                ),
                                _buildActionButton(
                                  'View Reply',
                                  Icons.rate_review_outlined,
                                  Colors.blue.shade700,
                                      () async {
                                    SharedPreferences sh = await SharedPreferences.getInstance();
                                    sh.setString('doid', did_[index]);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(builder: (context) => ViewReplyPage(title: 'View Reply')),
                                    );
                                  },
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ),
    );
  }
}