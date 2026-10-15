// Switch to database
use collegeDB

// Create collection
db.createCollection("students")

// CREATE - Insert one document
db.students.insertOne({
    roll: 1,
    name: "Raj",
    course: "CSE",
    marks: 85
})

// CREATE - Insert multiple documents
db.students.insertMany([
    {
        roll: 2,
        name: "Neha",
        course: "IT",
        marks: 90
    },
    {
        roll: 3,
        name: "Amit",
        course: "CSE",
        marks: 75
    }
])

// READ - Display all documents
db.students.find()

// READ - Find CSE students
db.students.find({
    course: "CSE"
})

// READ - Pretty format
db.students.find().pretty()

// UPDATE - Update Amit's marks
db.students.updateOne(
    { roll: 3 },
    { $set: { marks: 80 } }
)

// UPDATE - Add Pass status to CSE students
db.students.updateMany(
    { course: "CSE" },
    { $set: { status: "Pass" } }
)

// READ - Verify updates
db.students.find().pretty()

// DELETE - Delete student with roll 2
db.students.deleteOne({
    roll: 2
})

// DELETE - Delete students with Fail status
db.students.deleteMany({
    status: "Fail"
})

// READ - Verify final documents
db.students.find().pretty()

// AGGREGATION - Average marks by course
db.students.aggregate([
    {
        $group: {
            _id: "$course",
            avgMarks: { $avg: "$marks" }
        }
    }
])