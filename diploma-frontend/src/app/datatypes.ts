export interface LogItem {
    uuid: String
    created_at: String
    faces_number: number
    message: String
    image: Image
}

export interface Session {
    session_id: String
    created_at: String
    finished_at: String
    is_active: boolean
}

export interface Image {
    uuid: String
    image: String
}