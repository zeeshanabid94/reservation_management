import React from 'react';
import moment from 'moment';
import '../../App.css';
import './calendar.css';
import { reservationGet } from './mocked_data/reservations';
import { FormTextInput, FormButton } from './../../components/input_elements/input_elements'
import { Modal } from './../../components/modal/modal'
import { instanceOf } from 'prop-types';
import { withCookies, Cookies } from 'react-cookie';
let resourceUrlGet = "/reservations/.json";
let resourceUrlPost = "/reservations/";
let MONTHS = ["Jan", "Feb", "Apr", "Mar",
    "May", "Jun", "July", "Aug", "Sep",
    "Oct", "Nov", "Dec"];
let DAYS = ["Sunday", "Monday", "Tuesday",
    "Wednesday", "Thursday",
    "Friday", "Saturday"];
export class Calendar extends React.Component {
    static propTypes = {
        cookies: instanceOf(Cookies).isRequired
    }
    // Constructor for calendar
    constructor(props) {
        super(props);
        let current_time = moment();
        let time = moment(current_time).subtract(3, 'days');

        // Times for the calendar grid
        let grid = []
        for (let i = 0; i < props.length; i++) {
            let row = [];
            for (let j = 0; j < props.width; j++) {
                console.log(time.toString())
                row.push(moment(time));
                time = time.add(1, 'day');
            }
            grid.push(row);
        }

        // Binding methods
        this.onClickDay = this.onClickDay.bind(this);
        this.onReserve = this.onReserve.bind(this);
        this.onFullNameFieldChange = this.onFullNameFieldChange.bind(this);
        this.onEmailFieldChange = this.onEmailFieldChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.onCloseModal = this.onCloseModal.bind(this);

        // Setting state
        this.state = {
            current: current_time,
            grid_length: props.length,
            grid_width: props.width,
            grid: grid,
            start_day: null,
            end_day: null,
            csrf: props.cookies.get("csrftoken"),
            modalShow: false,
            fullname: null,
            email: null
        }
    }

    // Here we fetch data from Django Backend
    componentDidMount() {
        let newState = this.state;
        fetch(resourceUrlGet)
            .then((res) => {
                console.log(res.statusText);
                console.log(res.status);
                return res.json();
            })
            .then((json_results) => {
                let reservations = [];
                let res = json_results;
                for (let i = 0; i < res.length; i++) {
                    reservations.push([moment.unix(res[i].start_date), moment.unix(res[i].end_date)]);
                }

                console.log("RESERVATIONS", reservations)
                newState.reservations = reservations;
                this.setState(newState);
            })
            .catch((err) => {
                console.log(err.toString());
                console.log("AN error occurred while fetching data.");
            })

    }

    // Called when close in modal is pressed.
    onCloseModal() {
        console.log("Close Modal");
        let newState = this.state;
        newState.modalShow = false;
        this.setState(newState);
    }

    // Fullname field onchange callback
    onFullNameFieldChange(event) {
        let newState = this.state;
        newState.fullname = event.target.value.toLowerCase();
        this.setState(newState);
    }

    // Email field onchange callback
    onEmailFieldChange(event) {
        let newState = this.state;
        console.log(event.target.value)
        newState.email = event.target.value.toLowerCase();
        this.setState(newState);
    }

    // Form Submit and button onClick callback
    onSubmit() {
        console.log("Submitted");
        let data = {
            fullname: this.state.fullname,
            email: this.state.email,
            start_date: this.state.start_day.unix(),
            end_date: this.state.end_day.unix()
        }
        console.log("Payload", data);
        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'X-CSRFToken': this.state.csrf
        }
        fetch(resourceUrlPost, {
            method: "POST",
            body: JSON.stringify(data),
            headers: headers
        })
            .then((response) => {
                console.log(response.status);
                console.log(response.statusText);
                console.log(response.json())
                return response;
            })
            .catch((err) => {
                console.log(err.toString());
                console.log("Unable to reserve");
            })
    }

    // onClick callback for reserve button
    onReserve() {
        console.log("Reserving", this.state.start_day.toString(), this.state.end_day.toString());

        if (this.state.start_day === null) {
            console.log("Start date is null.");
        } else if (this.state.end_day === null) {
            console.log("End date is null");
        } else {
            // Show Modal here.
            let newState = this.state;
            newState.modalShow = true;
            this.setState(newState);

        }
    }

    // onClick one day on grid callback
    onClickDay(aMoment) {
        console.log("PRESSED", aMoment.toString());
        let newState = this.state;
        if (newState.start_day != null && newState.end_day != null) {
            newState.start_day = aMoment;
            newState.end_day = null;
        } else if (newState.start_day == null) {
            newState.start_day = aMoment;
        } else {
            if (newState.start_day.isBefore(aMoment, 'day')) {
                newState.end_day = aMoment;

                // Check if it overlaps with already done reservations
                for (let i = 0; i < this.state.reservations.length; i++) {
                    let reservation = this.state.reservations[i];

                    if (newState.start_day.isSameOrBefore(reservation[0], 'day') &&
                        newState.end_day.isSameOrAfter(reservation[1], 'day')) {
                        newState.start_day = aMoment;
                        newState.end_day = null;
                        break;
                    }
                }
            } else {
                newState.start_day = aMoment;
            }
        }
        this.setState(newState);
        console.log(newState);
    }

    // Reders the component.
    render() {
        console.log("Render State", this.state);
        let selected = false;
        let table_row_generator = (row, row_num) => {
            let dates = [];
            for (let j = 0; j < row.length; j++) {
                let locked = false;
                if (row[j].isBefore(moment(), 'day')) {
                    locked = true;
                }
                let taken = false;
                if (this.state.reservations) {
                    for (let k = 0; k < this.state.reservations.length; k++) {
                        if (row[j].isSameOrAfter(this.state.reservations[k][0], 'day') && row[j].isSameOrBefore(this.state.reservations[k][1], 'day')) {
                            console.log("TAKEN", row[j].toString());
                            taken = true;
                            break;
                        }
                    }
                }



                if (this.state.start_day && this.state.start_day.isSame(row[j], 'day')) {
                    selected = true;
                }

                dates.push(calender_day_generator(row[j].date(), row[j].month(), row[j].day(), locked, taken, selected, () => this.onClickDay(row[j])));

                if (this.state.end_day == null) {
                    selected = false;
                } else if (this.state.end_day && this.state.end_day.isSame(row[j], 'day')) {
                    selected = false;
                }
            }

            return (
                <tr>
                    {dates}
                </tr>
            )
        }

        let rows = []

        for (let i = 0; i < this.state.grid.length; i++) {
            rows.push(table_row_generator(this.state.grid[i], i));
        }
        let modalChildren = [
            <FormTextInput key='name' defaultValue='Enter your name here.' labelValue='Full Name' onChange={this.onFullNameFieldChange}></FormTextInput>,
            <FormTextInput key='email' defaultValue='Enter your name here.' labelValue='Email' onChange={this.onEmailFieldChange}></FormTextInput>,
            <FormButton key='confirm' labelValue="Confirm" onSubmit={this.onSubmit}></FormButton>
        ]
        let modal = <Modal onClose={this.onCloseModal} show={this.state.modalShow} children={modalChildren} heading="Reservation Confirmation"></Modal>
        console.log(modal);
        return (
            <div id="calendar_app">
                {modal}
                <h1>
                    Calendar
                </h1>
                <div class="calendar">
                    <h2 class="year">
                        2018
                    </h2>
                    <div class="dates">
                        <table class="dates_table">
                            {rows}
                        </table>
                    </div>
                    <button class="reserve_button" onClick={this.onReserve}>
                        Reserve
                    </button>
                </div>
            </div>
        )
    }
}

let calender_day_generator = ((date, month, day, locked, taken, selected, onClick) => {
    if (locked === true) {
        return (
            <td class="date_entry border_bottom border_right locked">
                <div class="date">
                    {date} {MONTHS[month]}
                </div>
                <div class="day">
                    {DAYS[day]}
                </div>
            </td>
        )
    } else if (taken === true) {
        return (
            <td class="date_entry border_bottom border_right reserved">
                <div class="date">
                    {date} {MONTHS[month]}
                </div>
                <div class="day">
                    {DAYS[day]}
                </div>
            </td>
        )
    } else if (selected === true) {
        return (
            <td class="date_entry border_bottom border_right selected">
                <div class="date">
                    {date} {MONTHS[month]}
                </div>
                <div class="day">
                    {DAYS[day]}
                </div>
            </td>
        )
    } else {
        return (
            <td class="date_entry border_bottom border_right" onClick={onClick}>
                <div class="date">
                    {date} {MONTHS[month]}
                </div>
                <div class="day">
                    {DAYS[day]}
                </div>
            </td>
        )

    }
}


);

export default withCookies(Calendar);