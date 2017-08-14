package com.example.miles.hw6;





import android.content.ContentValues;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.location.Location;
import android.media.RingtoneManager;
import android.provider.BaseColumns;
import android.support.annotation.Nullable;
import android.support.v4.content.ContextCompat;
import android.support.v4.widget.SimpleCursorAdapter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.FragmentTransaction;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.ViewAnimator;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationListener;

import org.w3c.dom.Text;


public class MainActivity extends AppCompatActivity implements
        GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener {


    private static final int LOCATION_PERMISSION_RESULT = 0;
    private FusedLocationProviderClient mFusedLocationClient;
    private LocationRequest mLocationRequest;
    private GoogleApiClient mGoogleApiClient;
    private TextView mLatText;
    private TextView mLonText;
    private TextView saLon1;
    private TextView saLon2;
    private TextView saLon3;
    private TextView saLon4;
    private TextView saLon5;
    private TextView saLon6;
    private TextView saLat1;
    private TextView saLat2;
    private TextView saLat3;
    private TextView saLat4;
    private TextView saLat5;
    private TextView saLat6;
    private Button button;
    private int count;
    private SQLiteDB mSQLiteExample;
    private SQLiteDatabase mSQLDB;

    private Cursor mSQLCursor;
    private SimpleCursorAdapter mSQLCursorAdapter;

    private Location mLastLocation;
    private LocationListener mLocationListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        count = 0;
        mSQLiteExample = new SQLiteDB(this);
        mSQLDB = mSQLiteExample.getWritableDatabase();

        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);

        if (mGoogleApiClient == null) {
            mGoogleApiClient = new GoogleApiClient.Builder(this)
                    .addConnectionCallbacks(this)
                    .addOnConnectionFailedListener(this)
                    .addApi(LocationServices.API)
                    .build();
        }

        mLatText = (TextView) findViewById(R.id.mLatText);
        mLonText = (TextView) findViewById(R.id.mLonText);
        mLatText.setText("Hello World!");

        saLat1 = (TextView) findViewById(R.id.saLat1);
        saLat2 = (TextView) findViewById(R.id.saLat2);
        saLat3 = (TextView) findViewById(R.id.saLat3);
        saLat4 = (TextView) findViewById(R.id.saLat4);
        saLat5 = (TextView) findViewById(R.id.saLat5);
        saLat6 = (TextView) findViewById(R.id.saLat6);

        saLon1 = (TextView) findViewById(R.id.saLon1);
        saLon2 = (TextView) findViewById(R.id.saLon2);
        saLon3 = (TextView) findViewById(R.id.saLon3);
        saLon4 = (TextView) findViewById(R.id.saLon4);
        saLon5 = (TextView) findViewById(R.id.saLon5);
        saLon6 = (TextView) findViewById(R.id.saLon6);

        mLocationRequest = LocationRequest.create();
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        mLocationRequest.setInterval(5000);
        mLocationRequest.setFastestInterval(5000);

        mLocationListener = new LocationListener() {
            @Override
            public void onLocationChanged(Location location) {
                if (location != null) {
                    mLonText.setText(String.valueOf(location.getLongitude()));
                    mLatText.setText(String.valueOf(location.getLatitude()));
                } else {
                    mLonText.setText("No Location Available");
                }
            }
        };

        Button activity1 = (Button) findViewById(R.id.submit);
        activity1.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                if(mSQLDB != null) {
                    ContentValues vals = new ContentValues();
                    vals.put(DBContract.DemoTable.COLUMN_NAME_LAT, mLatText.getText().toString());
                    vals.put(DBContract.DemoTable.COLUMN_NAME_LON, mLonText.getText().toString());
                    vals.put(DBContract.DemoTable.COLUMN_NAME_CNT, (String.valueOf(count)));
                    mSQLDB.insert(DBContract.DemoTable.TABLE_NAME, null, vals);
                    populate();
                    switch(count) {
                        case 0:
                            saLat1.setText(mLatText.getText());
                            saLon1.setText(mLonText.getText());
                            break;
                        case 1:
                            saLat2.setText(mLatText.getText());
                            saLon2.setText(mLonText.getText());
                            break;
                        case 2:
                            saLat3.setText(mLatText.getText());
                            saLon3.setText(mLonText.getText());
                            break;
                        case 3:
                            saLat4.setText(mLatText.getText());
                            saLon4.setText(mLonText.getText());
                            break;
                        case 4:
                            saLat5.setText(mLatText.getText());
                            saLon5.setText(mLonText.getText());
                            break;
                        case 5:
                            saLat6.setText(mLatText.getText());
                            saLon6.setText(mLonText.getText());
                            break;
                    }
                    count += 1;
                    if (count > 6){
                        count = 0;
                    }
                } else {
                    mLatText.setText("ERROR!");
                }

            }
        });

        mSQLCursor = mSQLDB.query(DBContract.DemoTable.TABLE_NAME,
                new String[]{DBContract.DemoTable.COLUMN_NAME_CNT, DBContract.DemoTable.COLUMN_NAME_LON, DBContract.DemoTable.COLUMN_NAME_LAT},
                DBContract.DemoTable.COLUMN_NAME_CNT + " >= ?",
                new String[] {"0"},
                null,
                null,
                null);

        populate();

    }

    public void populate(){
            for(mSQLCursor.moveToFirst(); !mSQLCursor.isAfterLast(); mSQLCursor.moveToNext()) {

                String cnt = mSQLCursor.getString(mSQLCursor.getColumnIndex(DBContract.DemoTable.COLUMN_NAME_CNT));
                String lat = mSQLCursor.getString(mSQLCursor.getColumnIndex(DBContract.DemoTable.COLUMN_NAME_LAT));
                String lon = mSQLCursor.getString(mSQLCursor.getColumnIndex(DBContract.DemoTable.COLUMN_NAME_LON));

                switch (Integer.parseInt(cnt)) {
                    case 0:
                        saLat1.setText(String.valueOf(lat));
                        saLon1.setText(String.valueOf(lon));
                        break;
                    case 1:
                        saLat2.setText(String.valueOf(lat));
                        saLon2.setText(String.valueOf(lon));
                        break;
                    case 2:
                        saLat3.setText(String.valueOf(lat));
                        saLon3.setText(String.valueOf(lon));
                        break;
                    case 3:
                        saLat4.setText(String.valueOf(lat));
                        saLon4.setText(String.valueOf(lon));
                        break;
                    case 4:
                        saLat5.setText(String.valueOf(lat));
                        saLon5.setText(String.valueOf(lon));
                        break;
                    case 5:
                        saLat6.setText(String.valueOf(lat));
                        saLon6.setText(String.valueOf(lon));
                        break;
                    case 6:
                        break;
                }
            }
    }

    @Override
    public void onStart() {
        mGoogleApiClient.connect();
        mLatText.setText("Connected to Google API");
        super.onStart();
    }

    @Override
    public void onStop(){
        mGoogleApiClient.disconnect();
        super.onStop();
    }

    @Override
    public void onConnected(@Nullable Bundle bundle){
        if (ActivityCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED &&
                ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, LOCATION_PERMISSION_RESULT);
            return;
        }
        updateLocation();

    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {
        if(requestCode == LOCATION_PERMISSION_RESULT){
            if(grantResults.length > 0){
                updateLocation();
            } else {
                mLatText.setText("44.5");
                mLonText.setText("-123.2");
                return;
            }
        }
    }

    private void updateLocation() {
        if (ActivityCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED &&
                ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED){
            mLatText.setText("44.5");
            mLonText.setText("-123.2");
            return;
        }

        mLastLocation = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);

        if(mLastLocation != null){
            mLatText.setText(String.valueOf(mLastLocation.getLatitude()));
            mLonText.setText(String.valueOf(mLastLocation.getLongitude()));
        } else {
            LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, mLocationListener);
        }
    }

    @Override
    public void onConnectionSuspended(int i) {

    }


    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {

    }

    final class DBContract {
        private DBContract(){};

        public final class DemoTable implements BaseColumns {
            public static final String DB_NAME = "hw6";
            public static final String TABLE_NAME = "hw6";
            public static final String COLUMN_NAME_LAT = "latitude";
            public static final String COLUMN_NAME_LON = "longitude";
            public static final String COLUMN_NAME_CNT = "count";
            public static final int DB_VERSION = 13;


            public static final String SQL_CREATE_DEMO_TABLE = "CREATE TABLE " +
                    DemoTable.TABLE_NAME + "(" +
                    DemoTable._ID + " INTEGER PRIMARY KEY NOT NULL, " +
                    DemoTable.COLUMN_NAME_LAT + " VARCHAR(255)," +
                    DemoTable.COLUMN_NAME_LON + " VARCHAR(255)," +
                    DemoTable.COLUMN_NAME_CNT + " INTEGER);";

            public  static final String SQL_DROP_DEMO_TABLE = "DROP TABLE IF EXISTS " + DemoTable.TABLE_NAME;
        }
    }


    class SQLiteDB extends SQLiteOpenHelper {

        public SQLiteDB(Context context) {
            super(context, DBContract.DemoTable.DB_NAME, null, DBContract.DemoTable.DB_VERSION);
        }

        @Override
        public void onCreate(SQLiteDatabase db) {
            db.execSQL(DBContract.DemoTable.SQL_CREATE_DEMO_TABLE);

            ContentValues testValues = new ContentValues();
            testValues.put(DBContract.DemoTable.COLUMN_NAME_LAT, "AH");
            testValues.put(DBContract.DemoTable.COLUMN_NAME_LON, "@#");
            testValues.put(DBContract.DemoTable.COLUMN_NAME_CNT, -1);
            db.insert(DBContract.DemoTable.TABLE_NAME,null,testValues);
        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            db.execSQL(DBContract.DemoTable.SQL_DROP_DEMO_TABLE);
            onCreate(db);
        }
    }


}


